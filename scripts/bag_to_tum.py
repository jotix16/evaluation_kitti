# uncompyle6 version 3.5.0
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.5 (default, Aug  7 2019, 00:51:29) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-39)]
# Embedded file name: /home/mzhobro/kitti_dataset/evaluation/scripts/bag_to_tum.py
# Compiled at: 2020-11-12 01:37:33
import os, numpy as np, rosbag, tf.transformations as tr
from evo.core.trajectory import PoseTrajectory3D
from evo.tools import file_interface
DESC = 'Combine KITTI poses and timestamps files to a TUM trajectory file'

def kitti_poses_and_timestamps_to_trajectory(poses_file, timestamp_file):
    pose_path = file_interface.read_kitti_poses_file(poses_file)
    raw_timestamps_mat = file_interface.csv_read_matrix(timestamp_file)
    error_msg = 'timestamp file must have one column of timestamps and same number of rows as the KITTI poses file'
    if len(raw_timestamps_mat) > 0 and len(raw_timestamps_mat[0]) != 1 or len(raw_timestamps_mat) != pose_path.num_poses:
        raise file_interface.FileInterfaceException(error_msg)
    try:
        timestamps_mat = np.array(raw_timestamps_mat).astype(float)
    except ValueError:
        raise file_interface.FileInterfaceException(error_msg)

    return PoseTrajectory3D(poses_se3=pose_path.poses_se3, timestamps=timestamps_mat)


def pq_to_transf(p, q):
    norm = np.linalg.norm(q)
    if np.abs(norm) < 1e-9:
        q = np.array([0.0, 0.0, 0.0, 1.0])
        print("oops 0 quaternion(q = {0:s} ".format(str(q)))
    elif np.abs(norm - 1.0) > 0.001:
        raise ValueError(('Received un-normalized quaternion (q = {0:s} ||q|| = {1:3.6f})').format(str(q), np.linalg.norm(q)))
    elif np.abs(norm - 1.0) > 1e-06:
        q = q / norm
    g = tr.quaternion_matrix(q)
    g[0:3, -1] = p
    return g[0:3, :]


def do_it(bag_file, topic_t, out_file, truth):
    timestamp_file = 'timestamps.txt'
    poses_file = '/tmp/kittie.kitti'
    timestamps = open(timestamp_file, 'w')
    offset = rosbag.Bag(bag_file).get_start_time()
    if truth:
        truth_timestamp_file = 'truth_timestamps.txt'
        truth_poses_file = '/tmp/truth_kittie.kitti'
        truth_timestamps = open(truth_timestamp_file, 'w')
        truth_outbag = open(truth_poses_file, 'w')
    with open(poses_file, 'w') as (outbag) :
        for topic, msg, t in rosbag.Bag(bag_file).read_messages():
            if topic == topic_t:
                timestamps.writelines([str(t.to_sec() - offset) + '\n'])
                p = np.array([msg.pose.pose.position.x, msg.pose.pose.position.y, msg.pose.pose.position.z])
                q = np.array([msg.pose.pose.orientation.x, msg.pose.pose.orientation.y, msg.pose.pose.orientation.z, msg.pose.pose.orientation.w])
                T = pq_to_transf(p, q)
                line = [ str(a) + ' ' for i in T for a in i ]
                line[-1] = line[(-1)].strip()
                line.append('\n')
                outbag.writelines(line)
            if topic == "/tf" and msg.transforms and truth:
                for m in msg.transforms:
                    if m.header.frame_id == "world" and m.child_frame_id == "base_link_gt":
                        truth_timestamps.writelines([str(t.to_sec() - offset) + '\n'])
                        p = np.array([m.transform.translation.x, m.transform.translation.y, m.transform.translation.z])
                        q = np.array([m.transform.rotation.x, m.transform.rotation.y, m.transform.rotation.z, m.transform.rotation.w])
                        T = pq_to_transf(p, q)
                        line = [ str(a) + ' ' for i in T for a in i ]
                        line[-1] = line[(-1)].strip()
                        line.append('\n')
                        truth_outbag.writelines(line)

    timestamps.close()
    trajectory = kitti_poses_and_timestamps_to_trajectory(poses_file, timestamp_file)
    os.remove(poses_file)
    os.remove(timestamp_file)
    file_interface.write_tum_trajectory_file(out_file, trajectory)

    if truth:
        truth_out_file = 'result/truth'
        truth_timestamps.close()
        truth_outbag.close()
        truth_trajectory = kitti_poses_and_timestamps_to_trajectory(truth_poses_file, truth_timestamp_file)
        os.remove(truth_poses_file)
        os.remove(truth_timestamp_file)
        file_interface.write_tum_trajectory_file(truth_out_file, truth_trajectory)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument('bag_file', help='bag path file in bag format')
    parser.add_argument('topic', help='topic for which to create a TUM file')
    parser.add_argument('trajectory_out', help='output file path for trajectory in TUM format')
    parser.add_argument('truth', nargs='?', default=False, help='offset to pring in measurement timeframe, time - offset')
    args = parser.parse_args()
    if args.truth:
        print("GEET TRUTH")
    do_it(args.bag_file, args.topic, args.trajectory_out, args.truth)