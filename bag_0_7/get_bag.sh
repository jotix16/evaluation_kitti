#!/bin/bash

# kitti2bag -t 2011_09_30 -r 0027 raw_synced
# mv kitti_2011_09_30_drive_0027_synced.bag bag/bag.bag
# python ../scripts/bl_to_bl_gt.py

# # get odom with rbtmap
# roslaunch get_odom.launch
# python ../scripts/bag_to_tum.py bag/odom.bag /rtabmap/odom result/odom True

# # run localization_fusion
# source ~/filter_ws/devel/setup.sh
# roslaunch launch.launch
# python ../scripts/bag_to_tum.py bag/loc_lib.bag /odometry/filtered result/loc_lib

# run robot_localization
# source ~/robloc_ws/devel/setup.sh
# roslaunch launch_robl.launch
# python ../scripts/bag_to_tum.py bag/rob_lib.bag /odometry/filtered_rob result/rob_lib


# evo_traj tum ./result/odom --ref=./result/truth --plot --plot_mode xyz -a --n_to_align 100 &
# evo_traj tum  ./result/loc_lib ./result/rob_lib --ref=./result/truth --plot --plot_mode xyz -a --n_to_align 100 &
# evo_traj tum ./result/rob_lib ./result/loc_lib --ref=./result/truth --plot --plot_mode xyz -a --n_to_align 100 &
# evo_traj tum ./result/odom ./result/rob_lib ./result/loc_lib --ref=./result/truth --plot --plot_mode xyz -a --n_to_align 100 &
# evo_traj tum  ./result/rob_lib --ref=./result/truth --plot --plot_mode xyz -a --n_to_align 100 &