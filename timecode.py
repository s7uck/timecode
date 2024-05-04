#!/usr/bin/python3

from time import sleep
import math
import mpv
import datetime
from os import path

time_format = '%p %H:%M:%S'

base_folder = path.dirname(__file__)

normal_beep = "*"
short_beep = "-"
low_beep = "_"
short_low_beep = "."
blank = " "
terminate = "\\"

chimes = {
    normal_beep: 'chime.ogg',
    short_beep: 'short_chime.ogg',
    low_beep: 'chime_low.ogg',
    short_low_beep: 'short_chime_low.ogg',
    blank: 'empty.ogg',
    terminate: 'terminate.ogg'
}


player = mpv.MPV()

def beep(symbol):
    player.play(path.join(base_folder, chimes[symbol]))
    player.wait_for_playback()

def blanking_interval():
    player.play(empty)
    player.wait_for_playback()
def signal_terminate():
    player.play(terminate)
    player.wait_for_playback()

def time_decode(s, separator=blank, hour_beep=normal_beep, minute_beep=normal_beep, minute_unit_beep=short_beep, second_beep=normal_beep, second_unit_beep=short_beep):
    hour = 0
    minute = 0
    second = 0
    daytime = 0

    signals = s.split(separator)
    for i, signal in enumerate(signals):
        if i == 0:
            daytime = signal.count(short_low_beep)
            hour = signal.count(hour_beep)
        if i == 1:
            minute = signal.count(minute_beep) * 5 + signal.count(minute_unit_beep)
        if i == 2:
            second = signal.count(second_beep) * 5 + signal.count(second_unit_beep)
    if daytime > 0: hour += 12

    return datetime.time(hour, minute, second)

def time_encode(time, separator=blank, hour_beep=normal_beep, minute_beep=normal_beep, minute_unit_beep=short_beep, second_beep=normal_beep, second_unit_beep=short_beep):
    hour = time.hour
    minute = time.minute
    second = time.second

    result = ""

    if hour == 0:
        result = 3 * low_beep

    if hour >= 7: result += short_low_beep
    if hour >= 12: result += short_low_beep
    if hour >= 20: result += short_low_beep

    hour12 = hour
    if hour > 12: hour12 = hour - 12

    minute12 = math.floor(minute / 5)
    minuteOffset = minute - (minute12 * 5)

    second12 = math.floor(second / 5)
    secondOffset = second - (second12 * 5)

    hour_beeps = hour_beep * hour12
    minute_beeps = minute_beep * minute12 + minute_unit_beep * minuteOffset
    second_beeps = second_beep * second12 + second_unit_beep * secondOffset

    result += hour_beeps + separator + minute_beeps + separator + second_beeps + terminate

    return result


def main(now=datetime.datetime.now().time()):
    time_string = time_encode(now, second_beep="", second_unit_beep="")
    if now.hour >= 7: print("·", end=" ")
    if now.hour >= 12: print("·", end=" ")
    if now.hour >= 20: print("·", end=" ")
    print(f"{now.hour:>02}:{now.minute:>02}:{now.second:>02}")
    for b in time_string:
        beep(b)
    print (time_string)
    return time_string

if __name__ == '__main__':
    import sys
    date = datetime.datetime.now().time()
    try:
        date = datetime.time(*[int(t) for t in sys.argv[1].split(":")])
    except: pass
    main(date)
