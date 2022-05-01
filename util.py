import numpy as np
import navpy as nv

from quad import Quadrotor
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

lat_ref,  lon_ref, alt_ref = 23.8621433, 90.3617857, 0


def set_axes_equal():
	'''Make axes of 3D plot have equal scale so that spheres appear as spheres,
	cubes as cubes, etc..  This is one possible solution to Matplotlib's
	ax.set_aspect('equal') and ax.axis('equal') not working for 3D.

	Input
	ax: a matplotlib axis, e.g., as output from plt.gca().
	'''
	ax = plt.gca()
	x_limits = ax.get_xlim3d()
	y_limits = ax.get_ylim3d()
	z_limits = ax.get_zlim3d()

	x_range = abs(x_limits[1] - x_limits[0])
	x_middle = np.mean(x_limits)
	y_range = abs(y_limits[1] - y_limits[0])
	y_middle = np.mean(y_limits)
	z_range = abs(z_limits[1] - z_limits[0])
	z_middle = np.mean(z_limits)

	# The plot bounding box is a sphere in the sense of the infinity
	# norm, hence I call half the max range the plot radius.
	plot_radius = 0.5*max([x_range, y_range, z_range])

	ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
	ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
	ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])

def show_drones(drones, ref):
    try:
        (lat_ref,  lon_ref, alt_ref) = ref
        plt.ion()
        fig = plt.figure('Drone Swarm')
        fig.canvas.mpl_connect('key_release_event',lambda event: [exit() if event.key == 'escape' else None])

        ax = fig.add_subplot(111, projection='3d')
        set_axes_equal()
        quads = []
        for _ in drones:
            quads.append(Quadrotor())
        while True:
            plt.cla()
            ax.set_xlabel('X Axis (M)')
            ax.set_ylabel('Y Axis(M')
            ax.set_zlabel('Z Axis(M)')
            ax.set_title('Swarm test')
            for index, drone in enumerate(drones):
                if drone.vehicle is not None:
                    lat, lon, alt = drone.vehicle.location.global_relative_frame.lat, drone.vehicle.location.global_relative_frame.lon, drone.vehicle.location.global_relative_frame.alt
                    x, y, z = nv.lla2ned(lat, lon, alt, lat_ref, lon_ref, alt_ref, latlon_unit='deg', alt_unit='m', model='wgs84')
                    roll, pitch, yaw =	drone.vehicle.attitude.roll, drone.vehicle.attitude.pitch, drone.vehicle.attitude.yaw
                    
                    p1_t, p2_t, p3_t, p4_t, x_data, y_data, z_data = quads[index].update_pose(x , y, -z, roll, pitch, yaw)
                    ax.scatter(x, y , -z, linewidth = 2.0, color='c')
                    ax.plot([p1_t[0], p2_t[0], p3_t[0], p4_t[0]],[p1_t[1], p2_t[1], p3_t[1], p4_t[1]],[p1_t[2], p2_t[2], p3_t[2], p4_t[2]], 'k.')
                    ax.plot([p1_t[0], p2_t[0]], [p1_t[1], p2_t[1]],[p1_t[2], p2_t[2]], 'r-')
                    ax.plot([p3_t[0], p4_t[0]], [p3_t[1], p4_t[1]],[p3_t[2], p4_t[2]], 'r-')
                    ax.plot(x_data, y_data, z_data, 'b:')
            set_axes_equal()
            plt.pause(0.001)
    except Exception as e:
	    plt.close('all')
