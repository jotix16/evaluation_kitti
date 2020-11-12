import rosbag
import os
from tf.msg import tfMessage

with rosbag.Bag('bag/bag_out.bag', 'w') as outbag:
    for topic, msg, t in rosbag.Bag('bag/bag.bag').read_messages():
        if topic == "/tf" and msg.transforms:
            newList = []
            for m in msg.transforms:
                if m.header.frame_id == "world":
                    m.child_frame_id = "base_link_gt"
                newList.append(m)
            if len(newList)>0:
                msg.transforms = newList
                outbag.write(topic, msg, t)
        elif topic == "/kitti/velo/pointcloud":
            pass
        else:
            outbag.write(topic, msg, t)