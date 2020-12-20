#Autor > Mikel Zhobro

import rosbag
import os
import numpy as np

DESC = 'Add noise to an Odometry topic in bag'


out_bag = 'bag_out223.bag'

def add_noise_odom(bagin, odom_topic, noise):
    print(noise)
    with rosbag.Bag(out_bag, 'w') as outbag:
        for topic, msg, t in rosbag.Bag(bagin).read_messages():
            if topic == odom_topic: #odom
                msg.pose.covariance = np.diag([noise[0]]*3+[noise[1]]*3).flatten().tolist()
                msg.twist.covariance = np.diag([noise[2]]*3+[noise[3]]*3).flatten().tolist()
            outbag.write(topic, msg, t)
    os.system("mv {} {}".format(out_bag, bagin))



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument('bag_file', help='bag path file in bag format')
    parser.add_argument('topic', help='topic for which to create a TUM file')
    parser.add_argument('--noise', action='store', type=float, nargs=4)

    args = parser.parse_args()


    add_noise_odom(args.bag_file, args.topic, args.noise)