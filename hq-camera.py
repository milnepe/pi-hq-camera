#!/usr/bin/python3

from gpiozero import DigitalOutputDevice, LED, Button
from signal import pause
from subprocess import check_call, Popen
from picamera import PiCamera
from datetime import datetime
from time import sleep

user = "yourusername"
remote_dir = "hostname:~/remotepath"
image_dir = "/home/pi/Pictures/"
video_dir = "/home/pi/Videos/"
filename = None

states = ['shutdown', 'still', 'video']
state = states[0]

Button.was_held = False
video_state = False

camera = PiCamera()

# Set pin 24 HIGH
led_power = DigitalOutputDevice(24, initial_value=True)
# State Indicator
led = LED(23)

# Set pin 17 HIGH
btn_power = DigitalOutputDevice(17, initial_value=True)
# Button with external pull down resistor
btn = Button(27, pull_up=None, active_state=True, hold_time=2)


def take_still():
    global filename
    print("click...")
    camera.stop_preview()
    filename = datetime.now().strftime('%Y%m%dT%H%M%S')
    # Take a shot
    camera.capture(f'{image_dir}{filename}.jpg')
    print(f'{image_dir}{filename}.jpg')

    # copy to remote dir using secure copy
    # Popen(f'scp {video_dir}{filename}.jpg {user}@{remote_dir}.jpg', shell=True)
    # print(f'image transfered...')

    # Re-start preview mode
    camera.start_preview()


def take_video():
    global video_state
    global filename
    if video_state is False:
        filename = datetime.now().strftime('%Y%m%dT%H%M%S')
        video_state = True
        print(f'start recording {filename}.h264')
        # record video to tmp dir
        camera.start_recording(f'/tmp/{filename}.h264')
    else:
        video_state = False
        camera.stop_recording()
        print("stop video...")
        sleep(2)
        # convert to mp4 and save in video dir
        Popen(f'MP4Box -add /tmp/{filename}.h264 {video_dir}{filename}.mp4', shell=True)
        print(f'Done encoding...')


def do_shutdown():
    print("shutdown...")
    check_call(['sudo', 'poweroff'])


def change_state():
    global state
    if state is 'shutdown':
        state = states[1]
        led.blink()
        camera.start_preview()
    elif state is 'still':
        state = states[2]
        led.blink(on_time=0.25, off_time=0.25)
        camera.start_preview()
    elif state is 'video':
        state = states[0]
        led.on()
        camera.stop_preview()
    print("state: ", state)


def op():
    global state
    if state is 'still':
        take_still()
    elif state is 'video':
        take_video()
    elif state is 'shutdown':
        do_shutdown()


def held(btn):
    btn.was_held = True
    print("button was held not just pressed")
    change_state()


def released(btn):
    if not btn.was_held:
        pressed()
    btn.was_held = False


def pressed():
    print("button was pressed not held")
    op()


def init_camera():
    camera.rotation = 270
    print("state: ", state)
    led.on()


init_camera()

btn.when_held = held
btn.when_released = released

pause()
