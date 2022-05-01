from math import cos, sin
import numpy as np


class Quadrotor():
	def __init__(self, x=0, y=0, z=0, roll=0, pitch=0, yaw=0, size=1.0):
		self.p1 = np.array([size / 2, 0, 0, 1]).T
		self.p2 = np.array([-size / 2, 0, 0, 1]).T
		self.p3 = np.array([0, size / 2, 0, 1]).T
		self.p4 = np.array([0, -size / 2, 0, 1]).T
		self.x = x
		self.y = y
		self.z = z
		self.roll = roll
		self.pitch = pitch
		self.yaw = yaw
		self.x_data = []
		self.y_data = []
		self.z_data = []
	def transformation_matrix(self):
		x = self.x
		y = self.y
		z = self.z
		roll = self.roll
		pitch = self.pitch
		yaw = self.yaw
		return np.array(
			[[cos(yaw) * cos(pitch),	-sin(yaw) * cos(roll) + cos(yaw) * sin(pitch) * sin(roll),		 sin(yaw) * sin(roll) + cos(yaw) * sin(pitch) * cos(roll),	 x],
			 [sin(yaw) * cos(pitch),	cos(yaw) * cos(roll) + sin(yaw) * sin(pitch)* sin(roll)	 ,		-cos(yaw) * sin(roll) + sin(yaw) * sin(pitch) * cos(roll),	 y],
			 [-sin(pitch)		   ,	cos(pitch) * sin(roll)									 ,		 cos(pitch) * cos(yaw)									 ,	 z]
			 ]
			 )


	def plot(self):	 # pragma: no cover
		T = self.transformation_matrix()
		p1_t = np.matmul(T, self.p1)
		p2_t = np.matmul(T, self.p2)
		p3_t = np.matmul(T, self.p3)
		p4_t = np.matmul(T, self.p4)
		return p1_t, p2_t, p3_t, p4_t


	def update_pose(self, x, y, z, roll, pitch, yaw):
		self.x = x
		self.y = y
		self.z = z
		self.roll = roll
		self.pitch = pitch
		self.yaw = yaw
		self.x_data.append(x)
		self.y_data.append(y)
		self.z_data.append(z)
		p1_t, p2_t, p3_t, p4_t = self.plot()
		return p1_t, p2_t, p3_t, p4_t, self.x_data, self.y_data, self.z_data