# -*- coding: utf-8 -*

import sys, wave, time
import pyaudio

v = sys.version_info[0]
if v == 2 :			# Pythonのバージョンに合わせたTkinterのimportを行う（このスクリプトでは2基準）
	import Tkinter
	import tkMessageBox
	import tkFileDialog
elif v == 3 :
	import tkinter as Tkinter
	from tkinter import messagebox as tkMessageBox
	from tkinter import filedialog as tkFileDialog
else :
	exit("*This script only supports Python2.x or 3.x.\nSorry, we can not support your Python.")

p = pyaudio.PyAudio()		# pyaudioの用意

def get_device() :			# pyaudioが認識できるマイク類を取得する
	global p

	devices = []
	for i in range(p.get_device_count()) :
		devices.append(p.get_device_info_by_index(i))

	names = []
	for i in devices :
		names.append(i["name"])

	return names
names = get_device()

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

root = Tkinter.Tk()
root.title("Select Device & Recording Time")
root.geometry("500x500")

#録音時間を設定する
#editbox = Tkinter.Entry()			# 入力ボックス
#editbox.pack()

#録音終了時間を設定する
label_time = Tkinter.Label(root, text="Finish Record Time")
label_time.pack()

box_hour = Tkinter.Entry(root, width=3)
box_hour.insert(Tkinter.END, 12)		# 初期入力値を設定する
box_hour.pack()

label_hour = Tkinter.Label(root, text="h")
label_hour.place(x=270, y=32)

box_minute = Tkinter.Entry(root, width=3)
box_minute.insert(Tkinter.END, 10)		# 初期入力値を設定する
box_minute.pack()

label_hour = Tkinter.Label(root, text="m")
label_hour.place(x=270, y=60)

# ラジオボタンを呼び出して，各ボタンに各デバイスを与える
var = Tkinter.IntVar()				# 最終的に，ここに選んだラジオボタンの値が格納される
for x, name in enumerate(names) :
	button = Tkinter.Radiobutton(root, text=name, variable=var, value=x)
	button.pack()

# 録音開始のボタンを用意する．
# root.quit()でroot.mainloop()の外＝その後のコード実行
end_button = Tkinter.Button(root, text="Start Recoding", command=root.quit)
end_button.pack()

root.mainloop()

# 入力/選択した値を取得する
#sec = editbox.get()
end_time = (int(box_hour.get()), int(box_minute.get()))
index = var.get()			# 選んだラジオボタンに呼応した値


# 録音設定
CHUNK = 1024
FORMAT = pyaudio.paInt16 # int16型
CHANNELS = 2             # ステレオ
RATE = 44100             # 441.kHz
WAVE_OUTPUT_FILENAME, RECORD_SECONDS = rec_time()
WAVE_OUTPUT_FILENAME += ".wav"

#RECORD_SECONDS = 10

stream = p.open(	format=FORMAT, 
					channels=CHANNELS, 
					rate=RATE, 
					input=True, 
					frames_per_buffer=CHUNK, 
					input_device_index=index,
				)

print("* recording")

frames = []

start_time = time.time()
time_flag = 1

while True :
	data = stream.read(CHUNK)
	frames.append(data)

	check_t = time.localtime()
	if check_t.tm_hour == end_time[0] and check_t.tm_min >= end_time[1]:
		break


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