#!/bin/bash

rtabmap-kitti_dataset \
       --Rtabmap/PublishRAMUsage true\
       --Rtabmap/DetectionRate 2\
       --Rtabmap/CreateIntermediateNodes true\
       --RGBD/LinearUpdate 0\
       --GFTT/QualityLevel 0.01\
       --GFTT/MinDistance 7\
       --OdomF2M/MaxSize 3000\
       --Mem/STMSize 30\
       --Kp/MaxFeatures 750\
       --Vis/MaxFeatures 1500\
       --gt ../ground_truth/poses/02.txt\
       ./2011_10_03/2011_10_03_drive_0034_sync