import rosbag
import os
from tf.msg import tfMessage
from nav_msgs.msg import Odometry

with rosbag.Bag('bag/bag_out.bag', 'w') as outbag:
    for topic, msg, t in rosbag.Bag('bag/bag.bag').read_messages():
        if topic == "/tf" and msg.transforms:
            newList = []
            for m in msg.transforms:
                if m.header.frame_id == "world":
                    m.child_frame_id = "base_link_gt"
                    odom_gt = Odometry()
                    odom_gt.header = m.header
                    odom_gt.header.frame_id = 'world'
                    odom_gt.child_frame_id = 'base_link_gt'
                    odom_gt.pose.pose.position = m.transform.translation
                    odom_gt.pose.pose.orientation = m.transform.rotation
                    outbag.write("/odom_gt", odom_gt, t)
                newList.append(m)
            if len(newList)>0:
                msg.transforms = newList
                outbag.write(topic, msg, t)
        else:
            outbag.write(topic, msg, t)