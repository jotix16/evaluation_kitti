#!/bin/bash

# kitti2bag -t 2011_09_30 -r 0016 raw_synced
# mv kitti_2011_09_30_drive_0016_synced.bag bag/bag.bag

# get odom with rbtmap
# roslaunch get_odom.launch
# evo_traj bag ./bag/odom.bag /rtabmap/odom --save_as_kitti
# mv ./odom.kitti ./result/odom.kitti

# run localization_fusion
roslaunch launch.launch
evo_traj bag ./bag/loc_lib.bag /odometry/filtered --save_as_kitti
mv ./filtered.kitti ./result/loc_lib.kitti

# run robot_localization
roslaunch launch_robl.launch
evo_traj bag ./bag/rob_lib.bag /odometry/filtered_rob --save_as_kitti
mv ./filtered_rob.kitti ./result/rob_lib.kitti


evo_traj kitti ./result/loc_lib.kitti ./result/odom.kitti ./result/rob_lib.kitti --ref=./result/04.txt --plot --plot_mode xyz -a --n_to_align 229