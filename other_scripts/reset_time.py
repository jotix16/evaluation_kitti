#Autor > Mikel Zhobro

import os, numpy as np, rosbag, tf.transformations as tr
from evo.core.trajectory import PoseTrajectory3D
from evo.tools import file_interface
import rospy
DESC = 'Combine KITTI poses and timestamps files to a TUM trajectory file'

POSE_COV = 0.3
TWIST_COV = 0.5


def do_it(bag, full_bag, thetopic):
    print('Bag:', bag)
    print('Output Bag:', "t_"+bag.split('/')[-1])
    with rosbag.Bag("t_"+bag.split('/')[-1], 'w') as outbag :
        odom_start_time = 0.0
        gt_odom_start_time = 0.0
        got_first_odom = False
        got_gt_first_odom = False
        for topic, msg, t in rosbag.Bag(bag).read_messages():
            if got_first_odom and got_gt_first_odom:
                break
            if not got_first_odom and topic in ["/odom"]:
                odom_start_time = msg.header.stamp
            if not got_gt_first_odom and topic in ["/gt_odom"]:
                gt_odom_start_time = msg.header.stamp
        offset = odom_start_time - gt_odom_start_time
        for topic, msg, t in rosbag.Bag(bag).read_messages():
            if topic not in ["/odom"]:
                msg.header.stamp = msg.header.stamp + offset
            else:
                msg.pose.covariance = (POSE_COV*np.eye(6)).reshape(1,-1).tolist()[0][:]
                msg.twist.covariance = (TWIST_COV*np.eye(6)).reshape(1,-1).tolist()[0][:]
            outbag.write(topic, msg, t)

        imu_start_time = 0.0
        for topic, msg, t in rosbag.Bag(full_bag).read_messages(topics=thetopic):
            imu_start_time = msg.header.stamp
            break

        offset = odom_start_time - imu_start_time
        for topic, msg, t in rosbag.Bag(full_bag).read_messages(topics=thetopic):
            if topic == thetopic:
                msg.header.stamp += offset
                msg.angular_velocity_covariance = (POSE_COV*np.eye(3)).reshape(1,-1).tolist()[0][:]
                msg.linear_acceleration_covariance = (POSE_COV*np.eye(3)).reshape(1,-1).tolist()[0][:]
                msg.orientation_covariance = (POSE_COV*np.eye(3)).reshape(1,-1).tolist()[0][:]
                outbag.write(topic, msg, t)







if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument('bag_files', help='paths to bags to be reseted')
    parser.add_argument('full_bag', help='paths to full bag with imu topic')
    parser.add_argument('topic', help='paths to bags to be reseted')
    args = parser.parse_args()

    do_it(args.bag_files, args.full_bag, args.topic)