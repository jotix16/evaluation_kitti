import rosbag
import numpy as np
import tf.transformations as tr

from evo.core.trajectory import PoseTrajectory3D
from evo.tools import file_interface

DESC = "Combine KITTI poses and timestamps files to a TUM trajectory file"


def kitti_poses_and_timestamps_to_trajectory(poses_file, timestamp_file):
    pose_path = file_interface.read_kitti_poses_file(poses_file)
    raw_timestamps_mat = file_interface.csv_read_matrix(timestamp_file)
    error_msg = ("timestamp file must have one column of timestamps and same number of rows as the KITTI poses file")
    if len(raw_timestamps_mat) > 0 and len(raw_timestamps_mat[0]) != 1 or len(raw_timestamps_mat) != pose_path.num_poses:
        raise file_interface.FileInterfaceException(error_msg)
    try:
        timestamps_mat = np.array(raw_timestamps_mat).astype(float)
    except ValueError:
        raise file_interface.FileInterfaceException(error_msg)
    return PoseTrajectory3D(poses_se3=pose_path.poses_se3, timestamps=timestamps_mat)


def pq_to_transf(p, q):
    norm = np.linalg.norm(q)
    if np.abs(norm - 1.0) > 1e-3:
        raise ValueError(
            "Received un-normalized quaternion (q = {0:s} ||q|| = {1:3.6f})".format(
                str(q), np.linalg.norm(q)))
    elif np.abs(norm - 1.0) > 1e-6:
        q = q / norm
    g = tr.quaternion_matrix(q)
    g[0:3, -1] = p
    return g[0:3,:]

def do_it(bag_file, topic, out_file):
    timestamps = open('../result/timestamps.txt', 'w')
    with open('../result/loc_lib_out.kitti', 'w')  as outbag:
        for topic, msg, t in rosbag.Bag('loc_lib.bag').read_messages():
            if topic == "/odometry/filtered":
                print(t.to_sec())
                timestamps.writelines([str(t)+"\n"])
                p = np.array([msg.pose.pose.position.x, msg.pose.pose.position.y, msg.pose.pose.position.z])
                q = np.array([msg.pose.pose.orientation.x, msg.pose.pose.orientation.y,
                    msg.pose.pose.orientation.z, msg.pose.pose.orientation.w])
                T = pq_to_transf(p,q)
                line = [str(a)+" " for i in T for a in i ]
                line[-1] = line[-1].strip()
                line.append("\n")
                outbag.writelines(line)
            else:
                pass

    timestamps.close()




if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument("bag_file", help="bag path file in bag format")
    parser.add_argument("topic", help="topic for which to create a TUM file")
    parser.add_argument("trajectory_out", help="output file path for trajectory in TUM format")
    args = parser.parse_args()

    trajectory = kitti_poses_and_timestamps_to_trajectory(args.poses_file, args.timestamp_file)
    file_interface.write_tum_trajectory_file(args.trajectory_out, trajectory)
