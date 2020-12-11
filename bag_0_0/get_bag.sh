#!/bin/bash

# kitti2bag -t 2011_10_03 -r 0027 raw_synced
# mv kitti_2011_10_03_drive_0027_synced.bag bag/bag.bag
# python ../scripts/bl_to_bl_gt.py

## 1. Get odom with rbtmap( record imu and gps msgs too)
# roslaunch get_odom.launch
# python ../scripts/bag_to_tum.py bag/odom.bag /rtabmap/odom result/odom True

## Add noise to the imu measuremnets because they have 0 covariances
# python ../scripts/add_noise.py
# mv bag/out_final.bag bag/.odom

## 2. Get lidar odometry with loam
# python ../scripts/transform_times.py
# source ~/visual_odometry/devel/setup.sh
# roslaunch rf2o.launch
# python ../scripts/bag_to_tum.py bag/loam.bag /lidar/odom result/loam
# # python ../scripts/tum_to_bag.py # creates the bag with syncronized time_stamps and certain noise.


### CREATE THE BAG TO BE FUSED
# python ../scripts/topics_from_bags.py bag/odom.bag bag/loam.bag  bag/final_bag.bag  /rtabmap/odom /lidar/odom /kitti/oxts/imu
## 3. Run localization_fusion and create corresponding tum file for evaluation
# source ~/filter_ws/devel/setup.sh
# roslaunch launch.launch
# python ../scripts/bag_to_tum.py bag/loc_lib.bag /odometry/filtered result/loc_lib

## 4. Run robot_localization and create corresponding tum file for evaluation
# source ~/robloc_ws/devel/setup.sh
# roslaunch launch_robl.launch
# python ../scripts/bag_to_tum.py bag/rob_lib.bag /odometry/filtered_rob result/rob_lib

## Evaluate
# evo_traj tum ./result/rob_lib ./result/loc_lib ./result/odom --ref=./result/truth --plot # --plot_mode xyz -a --n_to_align 100

# echo "EVALUATE localization_fusion"
# evo_ape tum ./result/loc_lib ./result/truth --plot
# echo "EVALUATE robot_localization"
# evo_ape tum ./result/rob_lib ./result/truth --plot
# echo "EVALUATE visual odometry"
# evo_ape tum ./result/odom ./result/truth --plot
