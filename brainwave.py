# -*- coding: utf-8 -*

import time, sys
import thinkgear		# Pyserialが必要
import numpy as np
import cv2
import pandas as pd

import key_num as key

WINDOWNAME = "MindWave"
PORT = '/dev/tty.MindWaveMobile-DevA'	# PORTを$ls /dev/tty.*で確認しておく

STR_1 = "ASIC EEG Power: EEGPowerData("
STR_2 = ")"
STR_3 = ", "
NAME = np.array(["delta=", "theta=", "lowalpha=", "highalpha=", "lowbeta=", "highbeta=", "lowgamma=", "midgamma="])
#LABEL = np.array(["Flag, Hour", "Minute", "Second", "TimePassed", "Delta", "Theta", "Low_Alfa", "High_Alfa", "Low_Beta", "High_Beta", "Low_Gamma", "Mid_Gamma"])
LABEL = np.array(["Unix", "TimeStamp", "Delta", "Theta", "Low_Alfa", "High_Alfa", "Low_Beta", "High_Beta", "Low_Gamma", "Mid_Gamma"])

DEBUG = True
#DEBUG = False

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
	def __init__(self) :
		self.img1 = np.zeros([500, 500, 1])
		self.brain = np.zeros([1, LABEL.shape[0]])

	def set(self) :
		self.th = thinkgear.ThinkGearProtocol(PORT)
		self.think = self.th.get_packets()
		print(self.think)

	def make_zero(self, value) :
		out = str(value)
		if value < 10 :
			out = out.zfill(2)				# 桁揃え
		return out

	def brainwave(self, p) :
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
	
		out = np.array([result])
		if DEBUG :
			print(out)
		return out

	def csv(self, name="brain") :							# CSV形式で保存
		v = self.brain[1:]
		c = LABEL
		df = pd.DataFrame(v, columns=c)
		df.to_csv(name+".csv", index=False, encoding="utf-8")

	def finish(self) :						# 終了処理
		cv2.destroyAllWindows()
		self.th.io.close()
		self.th.serial.close()
		sys.exit()

	def main(self) :
		self.set()
		start_time = time.time()
		csv_flag = 1

		for packets in self.think:
			for p in packets:
				if isinstance(p, thinkgear.ThinkGearRawWaveData):		# Rawデータを取り除く
					continue
				if isinstance(p, thinkgear.ThinkGearPoorSignalData):	# Poorシグナルを取り除く	
					continue
				if isinstance(p, thinkgear.ThinkGearAttentionData):		# Attention値を取り除く
					continue
				if isinstance(p, thinkgear.ThinkGearMeditationData):	# Meditation値を取り除く
					continue
				#if isinstance(p, thinkgear.ThinkGearEEGPowerData):		# フーリエ変換されたデータを取り除く	
				#	continue

				self.brain = np.append(self.brain, self.brainwave(p), axis=0)

				cv2.imshow(WINDOWNAME, self.img1)
				fps = int((1 - (time.time() - self.time_brain)) * 1000) - 100
				KEY = cv2.waitKey(fps)
				if KEY == key.esc :
					self.csv()
					self.finish()

				now_time = time.time()
				if now_time - start_time >= 10 * 60 :
					self.csv(name="brain_"+str(csv_flag))
					start_time = now_time
					csv_flag += 1
	
if __name__ == "__main__" :
	mind = Mind()
	mind.main()
