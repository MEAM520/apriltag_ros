#!/usr/bin/env python

from importlib.util import find_spec
from logging import lastResort
from re import S
import rospy
from apriltag_ros.msg import AprilTagDetectionArray
from copy import deepcopy

curr_reading = {'x':None, 'y':None, 'z':None}


def callback(data):
	global curr_reading
	for i in range(len(data.detections)):
		if data.detections[i].id[0] == 0:
			curr_reading['x'] = float(data.detections[i].pose.pose.pose.position.x)
			curr_reading['y'] = float(data.detections[i].pose.pose.pose.position.y)
			curr_reading['z'] = float(data.detections[i].pose.pose.pose.position.z)
		else:
			print("No tag 0 found!")

def listener():
	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber("tag_detections", AprilTagDetectionArray, callback)
	inp = None
	first_reading = None
	while inp!='q':
		inp = input("\nPress q to exit, any other for obs.")
		if first_reading is None:
			first_reading = deepcopy(curr_reading)
			print("\nLogged first block.\n")
		else:
			print("\nLogged second block.\n")
			dist = 0
			second_reading = deepcopy(curr_reading)
			print("--- Difference ---")
			for key in second_reading:
				print(key, ": ", (second_reading[key] - first_reading[key])*100)
				dist += ((second_reading[key] - first_reading[key])*100)**2
			print("Dist: ", dist**0.5)
			first_reading = deepcopy(curr_reading)

		
		



if __name__ == '__main__':
	listener()