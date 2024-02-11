import time
import math
import mpv
from datetime import datetime

time_format       = '%p %H:%M:%S'
normal_beep       = 'beep.ogg'
short_beep        = 'short_beep.ogg'
low_beep          = 'low_beep.ogg'
short_low_beep    = 'short_low_beep.ogg'
blanking_interval = 'empty.ogg'
signal_terminate  = 'terminate.ogg'

player = mpv.MPV()

def beep(type):
	player.play(type)

def blanking_interval():
	#player.play(blanking_interval)
	time.sleep(1)
def signal_terminate():
	#player.play(signal_terminate)
	time.sleep(0.5)

def write_time(time):
	hour = time.hour
	minute = time.minute
	second = time.second

	print(f"{hour > 12} {hour}:{minute}:{second}")

	if hour == 0 and minute == 0 and second == 0:
		beep(short_low_beep)
		beep(short_low_beep)
		beep(short_low_beep)
		signal_terminate()
		return

	if hour >= 7:
		beep(short_low_beep)
	if hour >= 12:
		beep(short_low_beep)
	if hour >= 20:
		beep(short_low_beep)

	hour12 = hour
	if hour > 12:
		hour12 = hour - 12

	minute12 = math.floor(minute / 5)
	minuteOffset = int(str(minute)[-1]) #sorry i couldn't figure out a better way right now

	second12 = math.floor(second / 5)
	secondOffset = int(str(second)[-1])

	for h in range(hour12):
		beep(normal_beep)

	blanking_interval()

	for m in range(minute12):
		beep(normal_beep)
	for n in range(minuteOffset):
		beep(short_beep)

	blanking_interval()

	for s in range(second12):
		beep(normal_beep)
	for t in range(secondOffset):
		beep(short_beep)

	blanking_interval()
	signal_terminate()
	return


def main():
	now = datetime.now()
	write_time(now)

if __name__ == '__main__':
	main()