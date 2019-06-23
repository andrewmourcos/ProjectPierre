# statistics requires python 3.4 atleast

import cv2
import numpy as np
import matplotlib.pyplot as plt
import statistics

class PoseEstimator():
	def __init__(self, webcam_num):
		self.body_parts = { "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4, 
		"LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9, "RAnkle": 10, "LHip": 11, 
		"LKnee": 12, "LAnkle": 13, "REye": 14, "LEye": 15, "REar": 16, "LEar": 17, "Background": 18 }

		self.pose_pairs = [ ["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"], 
		["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"], ["Neck", "RHip"], 
		["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"], ["LHip", "LKnee"], 
		["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],["REye", "REar"], ["Nose", "LEye"], 
		["LEye", "LEar"] ]

		self.net = cv2.dnn.readNetFromTensorflow("graph_opt.pb")
		self.cap = cv2.VideoCapture(webcam_num)

		self.frameWidth = 0
		self.frameHeight = 0

	def GetPose(self, frame):
		self.frameHeight = frame.shape[0]
		self.frameWidth = frame.shape[1]

		inWidth = 368
		inHeight = 368
		thr = 0.1

		self.net.setInput(cv2.dnn.blobFromImage(frame, 1.0, (inWidth, inHeight), (127.5, 127.5, 127.5), swapRB=True, crop=False))
		out = self.net.forward()
		out = out[:, :19, :, :]  # MobileNet output [1, 57, -1, -1], we only need the first 19 elements

		assert(len(self.body_parts) == out.shape[1])

		points = []
		for i in range(len(self.body_parts)):
		    # Slice heatmap of corresponging body's part.
		    heatMap = out[0, i, :, :]

		    # Originally, we try to find all the local maximums. To simplify a sample
		    # we just find a global one. However only a single pose at the same time
		    # could be detected this way.
		    _, conf, _, point = cv2.minMaxLoc(heatMap)
		    x = (self.frameWidth * point[0]) / out.shape[3]
		    y = (self.frameHeight * point[1]) / out.shape[2]
		    # Add a point if it's confidence is higher than threshold.
		    points.append((int(x), int(y)) if conf > thr else None)

		for pair in self.pose_pairs:
			partFrom = pair[0]
			partTo = pair[1]
			assert(partFrom in self.body_parts)
			assert(partTo in self.body_parts)

			idFrom = self.body_parts[partFrom]
			idTo = self.body_parts[partTo]

			font = cv2.FONT_HERSHEY_SIMPLEX

			if points[idFrom] and points[idTo]:
				cv2.putText(frame,str(idFrom),points[idFrom], font, 1,(255,255,255),2,cv2.LINE_AA)
				cv2.putText(frame,str(idTo),points[idTo], font, 1,(255,255,255),2,cv2.LINE_AA)

				cv2.line(frame, points[idFrom], points[idTo], (0, 255, 0), 3)
				cv2.ellipse(frame, points[idFrom], (3, 3), 0, 0, 360, (0, 0, 255), cv2.FILLED)
				cv2.ellipse(frame, points[idTo], (3, 3), 0, 0, 360, (0, 0, 255), cv2.FILLED)

		t, _ = self.net.getPerfProfile()
		freq = cv2.getTickFrequency() / 1000
		cv2.putText(frame, '%.2fms' % (t / freq), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

		cv2.imshow('yeet yeet', frame)
		return points

	@staticmethod
	def dist(tuple0, tuple1):
		return np.linalg.norm(tuple0-tuple1)

	def trackPose(self):
		queue = []
		vel_x=[]
		vel_y=[]
		fig = plt.gcf()
		fig.show()
		fig.canvas.draw()

		last_vel_y=0
		last_vel_x=0
		
		while cv2.waitKey(1) < 0:
			hasFrame, frame = self.cap.read()

			if not hasFrame:
				cv2.waitKey()
				break

			self.frameWidth = frame.shape[1]
			self.frameHeight = frame.shape[0]
			points = self.GetPose(frame)
			try:
				if len(queue) < 10:
					queue.append(points[0])
					x, y = zip(*queue)
					try:
						vel_x.append(list(x)[-1]-list(x)[-2])
						vel_y.append(list(y)[-1]-list(y)[-2])
					except:
						pass

				else:
					queue.pop(0)
					queue.append(points[0])
					x, y = zip(*queue)
					vel_x.pop(0)
					vel_y.pop(0)
					vel_x.append(list(x)[-1]-list(x)[-2])
					vel_y.append(list(y)[-1]-list(y)[-2])


				if (last_vel_y < 0 and list(x)[-1]-list(x)[-2] > 0) or (last_vel_y > 0 and list(x)[-1]-list(x)[-2] < 0):
					print("DING BRUH") 


				last_vel_x = list(x)[-1]-list(x)[-2]
				last_vel_y = list(y)[-1]-list(y)[-2]


				## med_x = statistics.median(x)
				## med_y = statistics.median(y)
				# med_x = 0
				# med_y = 0
				# x = [i - med_x for i in list(x)]
				# y = [i - med_y for i in list(y)]

				plt.clf()
				plt.plot(vel_x)
				plt.plot(vel_y)

				plt.xlim([0, 10])
				plt.ylim([-300, 300])

				fig.canvas.draw()
			except:
				pass

if __name__ == '__main__':
	poser = PoseEstimator(0)
	poser.trackPose()















