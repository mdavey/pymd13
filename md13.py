# https://github.com/superquadratic/rtmidi-python
# http://www.music.mcgill.ca/~gary/rtmidi/

import rtmidi_python as midi
import time

from event import Event


class SamsonMD13(object):
    EVENT_KEY_DOWN = 144
    EVENT_KEY_UP = 128
    EVENT_SLIDER = 176  # ??? I have no idea what this is called

    KEY_P1 = 36
    KEY_P2 = 37
    KEY_P3 = 38
    KEY_P4 = 39
    KEY_P5 = 40
    KEY_P6 = 41
    KEY_P7 = 42
    KEY_P8 = 43
    KEY_P9 = 44
    KEY_P10 = 45
    KEY_P11 = 46
    KEY_P12 = 47
    KEY_P13 = 48

    ENCODER_E1 = 16
    ENCODER_E2 = 17
    ENCODER_E3 = 18
    ENCODER_E4 = 19
    ENCODER_E5 = 20
    ENCODER_E6 = 21

    SLIDER_CROSS_FADE = 22
    SLIDER_STOP = 118
    SLIDER_PLAY_RECORD = 119

    OCTAVE = 12

    def __init__(self):
        self.midi_in = midi.MidiIn()
        self.port_num = None
        self.running = False

        self.onDown = Event()
        self.onUp = Event()
        self.onSlider = Event()
        self.onSliderStart = Event()
        self.onSliderEnd = Event()

    def open_port(self):
        for port_num, port_name in enumerate(self.midi_in.ports):
            if 'SAMSON Graphite MD13' in port_name:
                print 'Opening', port_name, 'on port', port_num
                self.port_num = port_num
                self.midi_in.open_port(port_num)
                return True
        return False

    def close_port(self):
        if self.port_num is not None:
            self.midi_in.close_port()

    def process_messages(self, message):
        event_num = message[0]
        event_key = message[1]

        if event_num == self.EVENT_KEY_DOWN:
            event_velocity = message[2]
            self.onDown(event_key, event_velocity)
        elif event_num == self.EVENT_KEY_UP:
            self.onUp(event_key)
        elif event_num == self.EVENT_SLIDER:
            event_position = message[2]  # 0-127
            self.onSlider(event_key, event_position)
        else:
            print 'Unknown message', message

    def start_message_loop(self, loop_sleep=0.001, slider_event_timeout=0.1):
        self.running = True
        slider_events = {}

        while self.running:
            (message, midi_time_offset) = self.midi_in.get_message()

            if message is not None:
                # Normal easy messages
                self.process_messages(message)

                # Now try to handle slider_start and slider_end events
                event_num = message[0]
                if event_num == self.EVENT_SLIDER:
                    slider_name = message[1]
                    slider_position = message[2]

                    if slider_name not in slider_events:
                        # First time we've seen this slider_name
                        self.onSliderStart(slider_name, slider_position)
                        slider_events[slider_name] = {'running': True, 'last_event': time.time(), 'last_value': slider_position}
                    elif slider_events[slider_name]['running']:
                        # slider_name still running
                        slider_events[slider_name] = {'running': True, 'last_event': time.time(), 'last_value': slider_position}
                    else:
                        # slider_name just started again
                        self.onSliderStart(slider_name, slider_position)
                        slider_events[slider_name] = {'running': True, 'last_event': time.time(), 'last_value': slider_position}

            # Now, every loop we check all the slider events to see if any have expired
            for slider_name in slider_events:
                if slider_events[slider_name]['running']:
                    if (time.time() - slider_events[slider_name]['last_event']) > slider_event_timeout:
                        self.onSliderEnd(slider_name, slider_events[slider_name]['last_value'])
                        slider_events[slider_name]['running'] = False

            time.sleep(loop_sleep)

    def stop_message_loop(self):
        self.running = False