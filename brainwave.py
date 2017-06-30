# -*- coding: utf-8 -*

import time, sys
if sys.version_info[0] == 2 :
	import thinkgear		# Pyserialが必要
else :
	exit("*This script only supports Python2.x.\nSorry, we can not support your Python.")

import numpy as np
import cv2
import pandas as pd

import key_num as key

WINDOWNAME = "MindWave"

STR_1 = "ASIC EEG Power: EEGPowerData("
STR_2 = ")"
STR_3 = ", "
STR_A = "ATTENTION eSense: "
STR_M = "MEDITATION eSense: "

NAME = np.array(["delta=", "theta=", "lowalpha=", "highalpha=", "lowbeta=", "highbeta=", "lowgamma=", "midgamma="])

X1, Y1 = 80, 300
X2, Y2 = 420, 470
X3, Y3 = X1, 100
X4, Y4 = X2, 200

def make_img() :
	global X1, X2, X3, X4
	global Y1, Y2, Y3, Y4

	black = (0, 0, 0)

	fontsize = 1.5
	font = cv2.FONT_HERSHEY_SIMPLEX
	thikness = 5
	if 
	linetype = cv2.CV_AA

	src = np.zeros([500, 500, 3], dtype=np.uint8)
	src.fill(255)

	cv2.rectangle(src, (X1, Y1), (X2, Y2), (180, 180, 180), -1)
	cv2.rectangle(src, (X1, Y1), (X2, Y2), black, 10)

	cv2.rectangle(src, (X3, Y3), (X4, Y4), (180, 180, 180), -1)
	cv2.rectangle(src, (X3, Y3), (X4, Y4), black, 10)

	cv2.putText(src, "Save Data", (120, 350), font, fontsize, black, thikness, linetype)
	cv2.putText(src, "&", (220, 400), font, fontsize, black, thikness, linetype)
	cv2.putText(src, "System Exit", (100, 450), font, fontsize, black, thikness, linetype)

	cv2.putText(src, "Save Data", (120, 170), font, fontsize, black, thikness, linetype)

	return src

def stamp() :
	t = time.localtime()
	stamp = [t.tm_hour, t.tm_min, t.tm_sec]
	out = ""
	for i in stamp :
		s = str(i)
		if i < 10 :
			s = "0" + s
		out += s
	return out

class Mind() :
	def __init__(self, port, debug=True, attention=False, meditation=False) :
		self.img = make_img()
		cv2.namedWindow(WINDOWNAME)
		cv2.setMouseCallback(WINDOWNAME, self.click)

		self.DEBUG = debug
		self.ATTENTION = attention
		self.MEDITATION = meditation
		
		self.label = np.array(["Unix", "TimeStamp", "Delta", "Theta", "Low_Alfa", "High_Alfa", "Low_Beta", "High_Beta", "Low_Gamma", "Mid_Gamma"])
		if attention :	
			self.label = np.append(self.label, "Attention")
		if meditation :
			self.label = np.append(self.label, "Meditation")

		self.param = {"port":port, "debug":debug, "attention":attention, "meditation":meditation}
		if debug :
			print(self.param)

		self.brain = np.zeros([1, self.label.shape[0]])

		self.th = thinkgear.ThinkGearProtocol(port)		# 接続
		self.think = self.th.get_packets()
		print(self.think)	

	def click(self, event, x, y, flags, param) :
		if event == cv2.EVENT_LBUTTONDOWN :		# 左クリックを検知
			if 	X1 <= x <= X2 and Y1 <= y <= Y2 :			# クリック位置が"Save Data & System Exitだった場合"
				self.csv()
				self.finish()
			elif X3 <= x <= X4 and Y3 <= y <= Y4 :			# クリック位置が"Save Data"だった場合
				self.csv(name=stamp())

	def brainwave(self) :
		p = self.psd

		p = str(p)					# pをstrに変換
		p = p.lstrip(STR_1)			# pから余分な文字を取り除く
		p = p.rstrip(STR_2)
		p = p.split(STR_3)			# pを", "で区切ってlist形式に

		t = time.localtime()

		self.time_brain = time.time()
		result = [time.time(), stamp()]
		for x, i in enumerate(p) :
			out = i.lstrip(NAME[x])
			result.append(out)

		if self.ATTENTION :
			result.append(self.attention.lstrip(STR_A))
		if self.MEDITATION :
			result.append(self.meditation.lstrip(STR_M))
	
		out = np.array([result])
		if self.DEBUG :
			print(out)
		return out

	def csv(self, name="brain"+str(stamp())) :							# CSV形式で保存
		df = pd.DataFrame(self.brain[1:], columns=self.label)
		df.to_csv(name+".csv", index=False, encoding="utf-8")
		print("Save Data")

	def finish(self) :						# 終了処理
		cv2.destroyAllWindows()
		self.th.io.close()
		self.th.serial.close()
		sys.exit("System Exit")

	def main(self) :
		print("System Beginning")

		start_time = time.time()
		csv_flag = 1
		cnt = 0

		attention = meditation = ""

		for packets in self.think:
			for x, p in enumerate(packets):
				if x == 0 :
					time_fps = time.time()

				if isinstance(p, thinkgear.ThinkGearRawWaveData):		# Rawデータを取り除く
					continue

				if isinstance(p, thinkgear.ThinkGearPoorSignalData):	# Poorシグナルを取り除く	
					continue

				if isinstance(p, thinkgear.ThinkGearAttentionData):		# Attention値を取り除く
					if self.ATTENTION :
						self.attention = str(p)
						cnt += 1
					else :
						continue					

				if isinstance(p, thinkgear.ThinkGearMeditationData):	# Meditation値を取り除く
					if self.MEDITATION :
						self.meditation = str(p)
						cnt += 1
					else :
						continue

				if isinstance(p, thinkgear.ThinkGearEEGPowerData):		# フーリエ変換されたデータを取り除く	
					self.psd = str(p)
					cnt += 1

				if cnt == int(self.ATTENTION + self.MEDITATION + 1) :
					self.brain = np.append(self.brain, self.brainwave(), axis=0)
					cnt = 0

					cv2.imshow(WINDOWNAME, self.img)
					fps = int((1 - (time.time() - time_fps)) * 1000) - 100
					KEY = cv2.waitKey(fps)
					if KEY == key.esc :
						self.csv()
						self.finish()
					elif KEY == key.enter :
						self.csv(name=stamp())

					now_time = time.time()
					if now_time - start_time >= 10 * 60 :		# 10分経過したらバックアップ
						self.csv(name="brain_"+str(csv_flag))
						start_time = now_time
						csv_flag += 1

	
if __name__ == "__main__" :
	# portを$ls /dev/tty.*で確認しておく
	mind = Mind('/dev/tty.MindWaveMobile-DevA', attention=True, meditation=True)
	mind.main()
