#Autor > Mikel Zhobro

import rosbag
import os
import numpy as np
from tf.msg import tfMessage

or_cov = 0.2
vel_cov = 0.4
acc_cov = 0.4
out_bag = 'bag/bag1.bag'
with rosbag.Bag(out_bag, 'w') as outbag:
    for topic, msg, t in rosbag.Bag('bag/bag.bag').read_messages():
        if topic == '/kitti/velo/pointcloud':
            msg.header.frame_id = "/camera_init"
            msg.fields[3].name = "intensity"
        outbag.write(topic, msg, t)