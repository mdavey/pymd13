# https://github.com/superquadratic/rtmidi-python
# http://www.music.mcgill.ca/~gary/rtmidi/

import rtmidi_python as midi

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

    def __init__(self):
        self.midi_in = midi.MidiIn()
        self.port_num = None
        self.onDown = Event()
        self.onUp = Event()
        self.onSlider = Event()

    def open_port(self):
        for port_num, port_name in enumerate(self.midi_in.ports):
            if 'SAMSON Graphite MD13' in port_name:
                print port_num, port_name
                self.port_num = port_num
                self.midi_in.open_port(port_num)
                return True
        return False

    def close_port(self):
        if self.port_num is not None:
            self.midi_in.close_port()

    def process_messages(self, message, time_stamp):
        event_num = message[0]
        event_key = message[1]
        print message
        if event_num == self.EVENT_KEY_DOWN:
            event_velocity = message[2]
            self.onDown(event_key, event_velocity)
        elif event_num == self.EVENT_KEY_UP:
            self.onUp(event_key)
        elif event_num == self.EVENT_SLIDER:
            event_position = message[2]  # 0-127
            self.onSlider(event_key, event_position)
        else:
            print message

    def start(self):
        self.midi_in.callback = lambda *args, **kwargs: self.process_messages(*args, **kwargs)

    def stop(self):
        self.midi_in.callback = None