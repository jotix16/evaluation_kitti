import os, numpy as np, rosbag, tf.transformations as tr
from evo.core.trajectory import PoseTrajectory3D
from evo.tools import file_interface
import rospy
import time

bag = "t_seq_0.bag"
for topic, msg, t in rosbag.Bag(bag).read_messages(topics = ["/odom"]):
    print(msg.header)
    break
for topic, msg, t in rosbag.Bag(bag).read_messages(topics = ["/kitti/oxts/imu", ]):
    print(msg.header)
    break