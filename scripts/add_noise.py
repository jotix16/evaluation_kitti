import rosbag
import os
import numpy as np
from tf.msg import tfMessage

or_cov = 0.2
vel_cov = 0.4
acc_cov = 0.4
out_bag = 'bag/out_final.bag'
with rosbag.Bag(out_bag, 'w') as outbag:
    for topic, msg, t in rosbag.Bag('bag/odom.bag').read_messages():
        if topic == '/kitti/oxts/imu':
            msg.orientation_covariance = (np.eye(3)*or_cov).reshape(1,-1).tolist()[0]
            msg.angular_velocity_covariance = (np.eye(3)*vel_cov).reshape(1,-1).tolist()[0]
            msg.linear_acceleration_covariance = (np.eye(3)*acc_cov).reshape(1,-1).tolist()[0]
        outbag.write(topic, msg, t)