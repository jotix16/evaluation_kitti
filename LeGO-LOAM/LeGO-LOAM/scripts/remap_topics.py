#!/usr/bin/python
# Autor> Mikel Zhobro

import time
import rospy
import math
import numpy as np
import tf.transformations as tr
import tf2_ros
from nav_msgs.msg import Odometry
# from tf2_msgs import TransformStamped
from tf2_geometry_msgs import *
from tf.transformations import *
from rospy.numpy_msg import numpy_msg


pub = None
pub_gt = None
ch_f_i = "base_link"
h_f_i = "odom"
position_covariance = 0.3
orientation_covariance= 0.2

R = np.zeros((3,3))
R[0,1] = 1
R[1,0] = 1
R[2,2] = 1

tfBuffer = None


def transform_odometry(odometry, trans):
	R = np.zeros((3,3))
	R[0,1] = 1
	R[1,0] = 1
	R[2,2] = 1
	T = np.eye(4)
	T[0:3,0:3] = R
	quat_trans = [trans.transform.rotation.x, trans.transform.rotation.y, trans.transform.rotation.z, trans.transform.rotation.w]
	quat_odom = [odometry.pose.pose.orientation.x, odometry.pose.pose.orientation.y, odometry.pose.pose.orientation.z, odometry.pose.pose.orientation.w]
	rot =  np.matmul(R, quaternion_matrix(quat_trans)[:3,:3])
	translation = np.array([trans.transform.translation.x, trans.transform.translation.y, trans.transform.translation.z]).reshape((3,1))

	# transform position
	position = np.matmul(rot, np.array([odometry.pose.pose.position.x, odometry.pose.pose.position.y, odometry.pose.pose.position.z]).reshape((3,1))) + translation
	# transform orientation
	quat_orient = quaternion_multiply(quat_trans, quat_odom)
	# quat_orient = quaternion_multiply(quaternion_from_matrix(T),36zk0 quat_orient)
	# transform pose covariance
	pose_cov = np.array(odometry.twist.covariance).reshape((6,6))
	pose_cov[:3, :3] = np.matmul(rot, pose_cov[:3, :3])
	pose_cov[:3, :3] = np.matmul(pose_cov[:3, :3], rot.T)
	pose_cov[-3:, -3:] = np.matmul(rot, pose_cov[-3:, -3:] )
	pose_cov[-3:, -3:] = np.matmul(pose_cov[-3:, -3:] , rot.T)

	# transform linear velocity
	linear = np.matmul(rot, np.array([odometry.twist.twist.linear.x, odometry.twist.twist.linear.y, odometry.twist.twist.linear.z]).reshape((3,1)))
	# transform linear velocity
	angular = np.matmul(rot, np.array([odometry.twist.twist.angular.x, odometry.twist.twist.angular.y, odometry.twist.twist.angular.z]).reshape((3,1)))
	# transform twist covariance
	twist_cov = np.array(odometry.twist.covariance).reshape((6,6))
	twist_cov[:3, :3] = np.matmul(rot, twist_cov[:3, :3])
	twist_cov[:3, :3] = np.matmul(twist_cov[:3, :3], rot.T)
	twist_cov[-3:, -3:] = np.matmul(rot, twist_cov[-3:, -3:] )
	twist_cov[-3:, -3:] = np.matmul(twist_cov[-3:, -3:] , rot.T)

	# Create the msg
	X = Odometry()
	X.header = odometry.header
	X.child_frame_id = odometry.child_frame_id
	X.pose.pose.position.x = position[0]
	X.pose.pose.position.y = position[1]
	X.pose.pose.position.z = position[2]
	X.pose.pose.orientation.x = quat_orient[0]
	X.pose.pose.orientation.y = quat_orient[1]
	X.pose.pose.orientation.z = quat_orient[2]
	X.pose.pose.orientation.w = quat_orient[3]
	X.twist.twist.linear.x = linear[0]
	X.twist.twist.linear.y = linear[1]
	X.twist.twist.linear.z = linear[2]
	X.twist.twist.angular.x = angular[0]
	X.twist.twist.angular.y = angular[1]
	X.twist.twist.angular.z = angular[2]
	X.pose.covariance = pose_cov.flatten().tolist()
	X.twist.covariance = twist_cov.flatten().tolist()
	return X

def odom_callback_loam(data):
	global pub
	global pub_gt
	global ch_f_i
	global h_f_i
	global tfBuffer
	data.header.frame_id = h_f_i
	data.child_frame_id = ch_f_i
	try:
		trans = tfBuffer.lookup_transform('base_link', 'camera_color_left', data.header.stamp)
		data_transformed = transform_odometry(data, trans)
		pub.publish(data_transformed)
	except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
		print("No transformation found")

def init():
	global pub
	global pub_gt
	global tfBuffer
	pub = rospy.Publisher('/odom_lidar', Odometry, queue_size=10)
	pub_gt = rospy.Publisher('/odom_gt', Odometry, queue_size=10)
	rospy.init_node('remap_topics')
	tfBuffer = tf2_ros.Buffer()
	listener = tf2_ros.TransformListener(tfBuffer)
	ch_f_i = rospy.get_param('~child_frame_id', 'odom')
	h_f_i = rospy.get_param('~frame_id', 'base_link')
	rospy.Subscriber('/integrated_to_init', Odometry, odom_callback_loam)
	# rospy.Subscriber('/laser_odom_to_init', Odometry, odom_callback_loam)

	print( ch_f_i, h_f_i)
	rospy.spin()

if __name__ == '__main__':
	init()
