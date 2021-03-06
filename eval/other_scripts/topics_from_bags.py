#Autor > Mikel Zhobro

import os, numpy as np, rosbag, tf.transformations as tr

DESC = 'Combine KITTI poses and timestamps files to a TUM trajectory file'

def do_it(bag_file1, bag_file2, out_bag, topics_):
    # out_bag  = 'out.bag'
    topics_temp = [t for t in topics_]
    with rosbag.Bag(out_bag, 'w') as outbag:
        for topic, msg, t in rosbag.Bag(bag_file1).read_messages(topics=topics_):
            if topic in topics_:
                outbag.write(topic, msg, t)

            if topic in topics_temp:
                topics_temp.remove(topic)

        for topic, msg, t in rosbag.Bag(bag_file2).read_messages(topics=topics_temp):
            if topic in topics_:
                outbag.write(topic, msg, t)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument('bag_file1', help='bag path1 file in bag format')
    parser.add_argument('bag_file2', help='bag path2 file in bag format')
    parser.add_argument('out_bag', help='bag path2 file in bag format')
    parser.add_argument('topics', nargs='+',help='topic for which to create a TUM file')
    args = parser.parse_args()
    do_it(args.bag_file1, args.bag_file2, args.out_bag, args.topics)