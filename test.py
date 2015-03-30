import time

from md13 import SamsonMD13


def handle_down(key, velocity):
    print 'DOWN', key, 'Velocity', velocity


def handle_up(key):
    print 'UP', key


def handle_slider(key, position):
    print 'SLIDER', key, position


def handle_exit(key, position):
    global running
    if key == SamsonMD13.SLIDER_STOP:
        running = False


md13 = SamsonMD13()
md13.onUp.append(handle_up)
md13.onDown.append(handle_down)
md13.onSlider.append(handle_slider)
md13.onSlider.append(handle_exit)

if md13.open_port():
    running = True
    md13.start()
    while running:
        try:
            time.sleep(0.100)
        except KeyboardInterrupt:
            running = False
    md13.stop()
    md13.close_port()