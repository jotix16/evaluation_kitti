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
# roslaunch visual_odom.launch

## 2. Get lidar odometry with loam
source ../../../../devel/setup.sh
roslaunch lidar_odom.launch
rosbag filter bag/loam.bag bag/fusion.bag 'topic != "/tf" or topic == "/tf" and m.transforms[0].header.frame_id == "world" and m.transforms[0].child_frame_id == "base_link_gt"'

## Add noise to the imu measuremnets because they have 0 covariances
python ../scripts/add_noise_to_imu.py bag/fusion.bag /kitti/oxts/imu --noise 0.4 0.3 0.5
python ../scripts/add_noise_to_odom.py bag/fusion.bag /odom_lidar --noise 0.8 0.5 1.5 1.6
rosbag info bag/fusion.bag

# cleanup
rm bag/loam.bag bag/bag_out.bag bag/odom.bag

## 3. Run localization_fusion and create corresponding tum file for evaluation
source ~/filter_ws/devel/setup.sh
roslaunch launch_loc.launch

## 4. Run robot_localization and create corresponding tum file for evaluation
source ~/robloc_ws/devel/setup.sh
roslaunch launch_robl.launch

## Evaluate
evo_traj bag bag/loc_lib.bag --all_topic --save_as_tum
mv *tum result/
evo_traj tum ./result/filtered.tum ./result/odom.tum ./result/odom_lidar.tum --ref=./result/odom_gt.tum --plot # --plot_mode xyz -a --n_to_align 100

# echo "EVALUATE localization_fusion"
evo_ape tum ./result/filtered.tum ./result/odom_gt.tum --plot
# echo "EVALUATE robot_localization"
# evo_ape tum ./result/rob_lib ./result/truth --plot
# echo "EVALUATE visual odometry"
# evo_ape tum ./result/odom ./result/truth --plot
