# -*- coding: utf-8 -*

import pyaudio
import wave, time

CHUNK = 1024
FORMAT = pyaudio.paInt16 # int16型
CHANNELS = 2             # ステレオ
RATE = 44100             # 441.kHz

def rec_time() :
	t = time.localtime()
	start = str(t.tm_year).lstrip("20")

	for i in (t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec) :
		if i >= 10 :
			start += str(i)
		else :
			start += "0" + str(i)

	base = 60 * 90			# 授業時間 60s * 90m
	b = (10, 40)
	begin = b[0] * 60 * 60 + b[1] * 60		# 開始時刻 10:40 = 10 * 60s * 60m + 40 * 60s
	now = t.tm_hour * 60 * 60 + t.tm_min * 60 + t.tm_sec
	dif = begin - now
	rec = base + dif

	return start, rec

WAVE_OUTPUT_FILENAME, RECORD_SECONDS = rec_time()
WAVE_OUTPUT_FILENAME += ".wav"

RECORD_SECONDS = 10

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

print("* recording")

frames = []

start_time = time.time()
time_flag = 1

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
	data = stream.read(CHUNK)
	frames.append(data)

	now_time = time.time()
	pass_time = now_time - start_time
	if pass_time >= 60 :
		print("%s min." %time_flag)
		time_flag += 1
		start_time = now_time

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()