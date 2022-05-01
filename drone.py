import time
import random
import navpy as nv
import numpy as np

from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationLocal

class Drone():
	def __init__(self, connection_string, idx):
		self.idx = idx
		self.connection_string = connection_string
		self.vehicle = None
	
	def connect(self):
		self.vehicle = connect(self.connection_string, wait_ready=True)

	# define function for take off
	def arm_and_takeoff(self, tgt_altitude=10):

		print(self.idx, " : Arming")

		while not self.vehicle.is_armable:
			time.sleep(1)
		while not self.vehicle.armed:
			print(self.idx, " : Waiting for arming...")
			self.vehicle.mode = VehicleMode("LOITER")

			self.vehicle.armed = True
			time.sleep(1)
		if self.vehicle.mode !=	 "GUIDED":
			self.vehicle.mode = VehicleMode("GUIDED")
			self.vehicle.simple_takeoff(tgt_altitude)
			print(self.idx, " : Takeoff")
		else:
			return
		# wait to reach the altitude
		while True:
			altitude = self.vehicle.location.global_relative_frame.alt
			if altitude >= tgt_altitude - 1:
				print(self.idx, " : Altitude Reached")
				break
			else:
				pass
			time.sleep(1)
			
	def test_goto(self, wp=None):
		lat_ref,  lon_ref, alt_ref = self.vehicle.location.global_relative_frame.lat, self.vehicle.location.global_relative_frame.lon, self.vehicle.location.global_relative_frame.alt
		self.arm_and_takeoff(alt_ref + 10)
		self.vehicle.airspeed = 10
		if wp is None:
			print(self.idx, " : Going to Random waypoint")
			lat, lon, alt = self.vehicle.location.global_relative_frame.lat, self.vehicle.location.global_relative_frame.lon, self.vehicle.location.global_relative_frame.alt

			lla = np.asarray([[lat, lon, alt]]).T
			x, y, z = nv.lla2ned(lat, lon, alt, float(lat_ref), float(lon_ref), float(alt_ref))

			x += (random.random()-0.5) * 20
			y += (random.random()-0.5) * 20
			z += abs((random.random()-0.5) * 20) + 5

			ned = [x, y, z]
			lat, lon, alt = nv.ned2lla(ned, lat_ref, lon_ref, alt_ref)
			wp = LocationGlobalRelative(lat, lon, alt)
			
		if self.vehicle.mode !=	 "GUIDED":
			self.vehicle.mode = VehicleMode("GUIDED")
			print(self.idx, " : Switching to GUIDED")

		self.vehicle.simple_goto(wp)
		time.sleep(10)
		print(self.idx, " : Coming back")
		self.vehicle.mode = VehicleMode("LAND")
		while  self.vehicle.armed:
			print("...", end='\r')
		self.vehicle.close()
		print(self.idx, " : Done")
	
	def test_run(self, wp):
		self.connect()
		self.test_goto(wp)
		
	def run(self):
		self.connect()
		self.arm_and_takeoff()
