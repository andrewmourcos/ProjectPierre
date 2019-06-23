# statistics requires python 3.4 atleast

import cv2
import numpy as np
import matplotlib.pyplot as plt
import statistics
import time


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
				# cv2.putText(frame,str(idFrom),points[idFrom], font, 1,(255,255,255),2,cv2.LINE_AA)
				# cv2.putText(frame,str(idTo),points[idTo], font, 1,(255,255,255),2,cv2.LINE_AA)

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
		head_queue = []
		r_arm_queue = []
		
		head_vel_x=[]
		head_vel_y=[]
		last_head_vel_y=0
		last_head_vel_x=0
		head_counter = 0

		r_arm_vel_x=[]
		r_arm_vel_y=[]
		last_r_arm_vel_y=0
		last_r_arm_vel_x=0
		r_arm_counter = 0

		fig = plt.gcf()
		fig.show()
		fig.canvas.draw()

		
		
		start = time.time()
		r_arm_start = time.time()

		while cv2.waitKey(1) < 0:
			hasFrame, frame = self.cap.read()

			if not hasFrame:
				cv2.waitKey()
				break

			self.frameWidth = frame.shape[1]
			self.frameHeight = frame.shape[0]
			points = self.GetPose(frame)
			try:
				if len(head_queue) < 10:
					head_queue.append(points[0])
					print(points[4])
					r_arm_queue.append(points[4])

					x, y = zip(*head_queue)
					x1, y1 = zip(*r_arm_queue)

					try:
						head_vel_x.append(list(x)[-1]-list(x)[-2])
						head_vel_y.append(list(y)[-1]-list(y)[-2])
					except:
						pass

					try:
						r_arm_vel_x.append(list(x1)[-1]-list(x1)[-2])
						r_arm_vel_y.append(list(y1)[-1]-list(y1)[-2])
					except:
						pass

				else:
					head_queue.pop(0)
					head_queue.append(points[0])
					r_arm_queue.pop(0)
					r_arm_queue.append(points[4])
					print(points[4])

					x, y = zip(*head_queue)
					x1, y1 = zip(*r_arm_queue)

					head_vel_x.pop(0)
					head_vel_y.pop(0)
					head_vel_x.append(list(x)[-1]-list(x)[-2])
					head_vel_y.append(list(y)[-1]-list(y)[-2])

					r_arm_vel_x.pop(0)
					r_arm_vel_y.pop(0)
					r_arm_vel_x.append(list(x1)[-1]-list(x1)[-2])
					r_arm_vel_y.append(list(y1)[-1]-list(y1)[-2])

				##### Moving Head #####
				if (last_head_vel_x < -2 and list(x)[-1]-list(x)[-2] > 2) or (last_head_vel_x > 2 and list(x)[-1]-list(x)[-2] < -2) or (last_head_vel_y < -2 and list(y)[-1]-list(y)[-2] > 2) or (last_head_vel_y > 2 and list(y)[-1]-list(y)[-2] < -2):
					if time.time() - start < 20:
						head_counter+=1
					else:
						start = time.time()
						head_counter=0

				if head_counter > 5:
					print("STOP MOVING YOUR HEAD!!!")
					head_counter = 0
					start = time.time()
				##### Moving Head #####


				##### Moving right arm #####
				if (last_r_arm_vel_x < -2 and list(x1)[-1]-list(x1)[-2] > 2) or (last_r_arm_vel_x > 2 and list(x1)[-1]-list(x1)[-2] < -2) or (last_r_arm_vel_y < -2 and list(y1)[-1]-list(y1)[-2] > 2) or (last_r_arm_vel_y > 2 and list(y1)[-1]-list(y1)[-2] < -2):
					if time.time() - r_arm_start < 20:
						r_arm_counter+=1
					else:
						r_arm_start = time.time()
						r_arm_counter=0

				if r_arm_counter > 5:
					print("STOP MOVING YOUR ARM!!!")
					r_arm_counter = 0
					r_arm_start = time.time()
				##### Moving right arm #####


				last_head_vel_x = list(x)[-1]-list(x)[-2]
				last_head_vel_y = list(y)[-1]-list(y)[-2]

				last_r_arm_vel_x = list(x1)[-1]-list(x1)[-2]
				last_r_arm_vel_y = list(y1)[-1]-list(y1)[-2]

				plt.clf()
				plt.plot(r_arm_vel_x)
				plt.plot(r_arm_vel_y)

				plt.xlim([0, 10])
				plt.ylim([-300, 300])

				fig.canvas.draw()
			except:
				pass

if __name__ == '__main__':
	poser = PoseEstimator(0)
	poser.trackPose()















