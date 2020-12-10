#!/bin/bash

## Download the dataset
# wget https://s3.eu-central-1.amazonaws.com/avg-kitti/raw_data/2011_09_30_drive_0016/2011_09_30_drive_0016_sync.zip
# unzip 2011_09_30_drive_0016_sync.zip
# rm 2011_09_30_drive_0016_sync.zip

## Download the calibration files
# wget https://s3.eu-central-1.amazonaws.com/avg-kitti/raw_data/2011_09_30_calib.zip
# unzip 2011_09_30_calib.zip
# rm 2011_09_30_calib.zip

## Create bag from the kitti dataset and map ground truth to /odom_gt
# kitti2bag -t 2011_09_30 -r 0016 raw_synced
# mv kitti_2011_09_30_drive_0016_synced.bag bag/bag.bag
# python ../scripts/bl_to_bl_gt.py

## 1. Get odom with rbtmap( record imu and gps msgs too)
# roslaunch get_odom.launch
# python ../scripts/bag_to_tum.py bag/odom.bag /rtabmap/odom result/odom True
# evo_traj bag bag/odom.bag /rtabmap/odom  /tf:world.base_link_gt --plot

## Add noise to the imu measuremnets because they have 0 covariances
# python ../scripts/add_noise.py
# mv bag/out_final.bag bag/.odom

## 2. Get lidar odometry with loam
# python ../scripts/transform_times.py
# source ~/visual_odometry/devel/setup.sh
# roslaunch rf2o.launch
python ../scripts/tum_to_bag.py # creates the bag with syncronized time_stamps and certain noise.

## 3. Run localization_fusion and create corresponding tum file for evaluation
# source ~/filter_ws/devel/setup.sh
# roslaunch launch.launch
# python ../scripts/bag_to_tum.py bag/loc_lib.bag /odometry/filtered result/loc_lib

## 4. Run robot_localization and create corresponding tum file for evaluation
# source ~/robloc_ws/devel/setup.sh
# roslaunch launch_robl.launch
# python ../scripts/bag_to_tum.py bag/rob_lib.bag /odometry/filtered_rob result/rob_lib

## Evaluate
evo_traj tum ./result/rob_lib ./result/loc_lib ./result/odom --ref=./result/truth --plot # --plot_mode xyz -a --n_to_align 100

# echo "EVALUATE localization_fusion"
# evo_ape tum ./result/loc_lib ./result/truth --plot
# echo "EVALUATE robot_localization"
# evo_ape tum ./result/rob_lib ./result/truth --plot
# echo "EVALUATE visual odometry"
# evo_ape tum ./result/odom ./result/truth --plot
