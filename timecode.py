#!/usr/bin/python3

from time import sleep
import math
import mpv
import datetime

time_format       = '%p %H:%M:%S'
normal_beep       = 'chime.ogg'
short_beep        = 'short_chime.ogg'
low_beep          = 'chime_low.ogg'
short_low_beep    = 'short_chime_low.ogg'
blanking_interval = 'empty.ogg'
signal_terminate  = 'terminate.ogg'

player = mpv.MPV()

def beep(b):
    print(b)
    player.play(b)
    player.wait_for_playback()

def blanking_interval():
    #player.play(blanking_interval)
    sleep(1)
def signal_terminate():
    #player.play(signal_terminate)
    sleep(0.5)

def write_time(time):
    hour = time.hour
    minute = time.minute
    second = time.second

    string = ""

    print(f"{hour > 12} {hour}:{minute}:{second}")

    if hour == 0:
        beep(low_beep)
        beep(low_beep)
        beep(low_beep)
        string = "___"

    if hour >= 7:
        beep(short_low_beep)
        string += "."
    if hour >= 12:
        beep(short_low_beep)
        string += "."
    if hour >= 20:
        beep(short_low_beep)
        string += "."

    hour12 = hour
    if hour > 12:
        hour12 = hour - 12

    minute12 = math.floor(minute / 5)
    minuteOffset = int(str(minute)[-1]) #sorry i couldn't figure out a better way right now

    second12 = math.floor(second / 5)
    secondOffset = int(str(second)[-1])

    print(hour12)
    for h in range(hour12):
        beep(normal_beep)
        string += "*"

    blanking_interval()
    string += " "

    print(minute12)
    for m in range(minute12):
        beep(normal_beep)
        string += "*"
    print(minuteOffset)
    for n in range(minuteOffset):
        beep(short_beep)
        string += "-"

    blanking_interval()
    string += " "

    print(second12)
    for s in range(second12):
        beep(normal_beep)
        string += "*"
    print(secondOffset)
    for t in range(secondOffset):
        beep(short_beep)
        string += "-"

    blanking_interval()
    signal_terminate()
    string += "  "
    return string


def main(now=datetime.datetime.now().time()):
    print(write_time(now))

if __name__ == '__main__':
    import sys
    date = datetime.datetime.now().time()
    try:
        date = datetime.time(*[int(t) for t in sys.argv[1].split(":")])
    except: pass
    main(date)
