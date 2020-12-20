#Autor > Mikel Zhobro

import tf.transformations as tr
import numpy as np
import os

row = [0,0,0,1]

R = np.eye(4)
t_imu_cam = np.array([1.1102242926728196, -0.31907194482240314, 0.7460658914035339]).reshape((3,-1))
t_bl_imu = np.array([-1.405, 0.32, 0.93]).reshape((3,-1))
R[0:3,0:3] = tr.quaternion_matrix([0.5042803291543856, -0.5003257925181871, 0.499074855710565676, -0.49628590285813])[0:3,0:3]
R[0:3,3:4] = t_bl_imu + t_imu_cam

ground_truth_path_input = "../ground_truth/poses/"
ground_truth_path_output = "../ground_truth/poses_bl/"

for seq in os.listdir(ground_truth_path_input):
    path_seq = os.path.join(ground_truth_path_input, seq)
    path_seq_out = os.path.join(ground_truth_path_output, seq)
    trajectory = np.loadtxt(path_seq)

    trajectory_bl = np.concatenate([trajectory.reshape(-1, 3, 4), np.expand_dims(np.tile(row,(trajectory.shape[0],1)), axis=1)], axis=1)
    trajectory_bl_out = np.einsum('tk,nkp->ntp', R, trajectory_bl)
    np.savetxt(path_seq_out, trajectory_bl_out[:,:3,:].reshape((1,trajectory_bl_out.shape[0],12))[0])
