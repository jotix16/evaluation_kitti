import os, numpy as np, rosbag, tf.transformations as tr
import rospy
from datetime import datetime

for path in os.listdir("."):
    if path.startswith("2011"):
        for spath in os.listdir(path):
            if spath.startswith("2011"):
                input_file = os.path.join(path, spath , "velodyne_points/timestamps.txt")
                output_file = os.path.join(path, spath , "velodyne_points/timestamps2.txt")
                print(input_file)
                print(output_file)

with open(output_file, 'w') as (outbag):
    with open(input_file, 'r') as (inbag):
        lines = inbag.readlines()
        for time_stamp in lines:
            if len(time_stamp) == 1:
                continue
            dt = datetime.strptime(time_stamp[:-4], '%Y-%m-%d %H:%M:%S.%f')
            line = str(rospy.Time.from_sec(float(datetime.strftime(dt, "%s.%f"))))
            outbag.writelines(line+"\n")
            # break