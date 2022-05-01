import time
import threading
import numpy as np
import navpy as nv
from util import show_drones
from drone import Drone



num_of_drones = 2
lat_ref,  lon_ref, alt_ref = None, None, None


print("Creating connection strings")
connection_strings = []
for idx in range(num_of_drones):
	connection_strings.append("tcp:127.0.0.1:" + str(5760 + idx * 10))
print("DONE")

print("Connecting to drones")
drones = []
for idx,connection_string in enumerate(connection_strings):
	drones.append(Drone(connection_string, idx))
print("DONE")

threads = []
print("Creating threads")
for drone in drones:
	threads.append(threading.Thread(target=drone.test_run, args=(None,),daemon=True))
print("DONE")

print("Starting threads")
for thread in threads:
	thread.start()
print("DONE")

while  drones[0].vehicle is None:
	time.sleep(1)

drone_leader = drones[0]
lat_ref,  lon_ref, alt_ref = drone_leader.vehicle.location.global_relative_frame.lat, drone_leader.vehicle.location.global_relative_frame.lon, drone_leader.vehicle.location.global_relative_frame.alt
ref = (lat_ref,  lon_ref, alt_ref)
#lat_ref,  lon_ref, alt_ref = 23.8621433, 90.3617857, 0

# blocks stuff
'''
for thread in threads:
	thread.join()
'''

print("Entering main loop")

try:
	show_drones(drones, ref)
except KeyboardInterrupt:
	print("Exiting script")
	exit()

print("DONE")
