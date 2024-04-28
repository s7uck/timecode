#!/usr/bin/python3

from time import sleep
import math
import mpv
import datetime

time_format = '%p %H:%M:%S'
chime = 'chime.ogg'
short_chime = 'short_chime.ogg'
chime_low = 'chime_low.ogg'
short_chime_low = 'short_chime_low.ogg'
empty = 'empty.ogg'
terminate = 'terminate.ogg'

normal_beep = "*"
short_beep = "-"
low_beep = "_"
short_low_beep = "."
blank = " "
terminate = "\\"


player = mpv.MPV()

def beep(b):
    player.play(b)
    player.wait_for_playback()

def blanking_interval():
    player.play(empty)
    player.wait_for_playback()
def signal_terminate():
    player.play(terminate)
    player.wait_for_playback()

def parse_timecode(s, separator=blank, hour_beep=normal_beep, minute_beep=normal_beep, minute_unit_beep=short_beep, second_beep=normal_beep, second_unit_beep=short_beep):
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

def beep_from_string(s):
    beeps = []
    for symbol in s:
        beeps.append({
            "*": chime,
            "-": short_chime,
            "_": chime_low,
            ".": short_chime_low,
            " ": empty,
            "\\": terminate
        }[symbol])
    return beeps

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
