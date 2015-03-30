import subprocess
from md13 import SamsonMD13

NIRCMD = r'c:\Program Files\nircmd\nircmdc.exe'


def handle_down(key, velocity):
    print 'DOWN', key, 'Velocity', velocity


def handle_up(key):
    print 'UP', key


def handle_slider(key, position):
    print 'SLIDER', key, position


def handle_slider_start(key, position):
    print 'SLIDER START', key, position


def handle_slider_end(key, position):
    print 'SLIDER END', key, position


def handle_exit(key, position):
    global running
    global md13
    if key == SamsonMD13.SLIDER_STOP:
        running = False
        md13.stop_message_loop()


def volume_control(key, position):
    if key == SamsonMD13.ENCODER_E6:
        windows_volume_setting = int(position/127.0 * 65535)
        print 'Setting volume to', windows_volume_setting
        subprocess.call([NIRCMD, 'setsysvolume', str(windows_volume_setting)])


md13 = SamsonMD13()
# md13.onUp.append(handle_up)
# md13.onDown.append(handle_down)
# md13.onSlider.append(handle_slider)
# md13.onSliderStart.append(handle_slider_start)
# md13.onSliderEnd.append(handle_slider_end)

md13.onSlider.append(handle_exit)
md13.onSliderEnd.append(volume_control)

if md13.open_port():
    md13.start_message_loop()