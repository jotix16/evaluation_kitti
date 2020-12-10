import os, numpy as np, rosbag, tf.transformations as tr
import rospy
from datetime import datetime
from nav_msgs.msg import Odometry
import tf.transformations as tr



os.system("rm bag/laser_odom.bag")

input_file = "LOAMTrajectory.tum"
out_bag = "bag/laser_odom.bag"
pose_cov = 0.1
orient_cov = 0.3

R_2 = np.eye(4)
R_2[0,0] = -1

R_3 = np.eye(4)
t_imu_cam = np.array([1.1102242926728196, -0.31907194482240314, 0.7460658914035339]).reshape((3,-1))
t_bl_imu = np.array([-1.405, 0.32, 0.93]).reshape((3,-1))
R_3[0:3,0:3] = tr.quaternion_matrix([0.5042803291543856, -0.5003257925181871, 0.499074855710565676, -0.49628590285813])[0:3,0:3]
R_3[0:3,3:4] = t_bl_imu + t_imu_cam

R = np.matmul(R_3, R_2)
print(R)

table = np.loadtxt(input_file)
with rosbag.Bag(out_bag, 'w') as (outbag):
    for line in table:
        time = line[0]
        position = np.matmul(R[0:3,0:3], line[1:4].reshape((3,1)))
        quat = line[4:]
        # print("Time: ", time)
        # print("Position: ", position)
        # print("Quaternion: ", quat)
        # print()
        quat  = tr.quaternion_from_matrix(np.matmul(R, tr.quaternion_matrix(quat)))
        topic = "/loam"
        msg = Odometry()
        msg.child_frame_id = "base_link"
        msg.header.frame_id = "odom"
        msg.header.stamp =  rospy.Time.from_sec(time)
        msg.pose.pose.position.x = position[0]
        msg.pose.pose.position.y = position[1]
        msg.pose.pose.position.z = position[2]
        msg.pose.pose.orientation.x = quat[0]
        msg.pose.pose.orientation.y = quat[1]
        msg.pose.pose.orientation.z = quat[2]
        msg.pose.pose.orientation.w = quat[3]

        cov = np.eye(6)
        cov[0:3,0:3] *= pose_cov
        cov[3:,3:] *= orient_cov
        msg.pose.covariance = cov.reshape((1,-1)).tolist()[0]
        outbag.write(topic, msg, msg.header.stamp)
# os.system("LOAMTrajectory.tum")
os.system("rm loam.kitti")
os.system("evo_traj bag bag/laser_odom.bag --all_topics --save_as_kitti")
os.system("evo_traj kitti odom.kitti loam.kitti --plot")
# os.system("evo_traj bag bag/laser_odom.bag --all_topics --save_as_tum")
# os.system("evo_traj tum result/truth loam.tum --plot")