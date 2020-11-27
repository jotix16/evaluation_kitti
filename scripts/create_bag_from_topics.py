import os, numpy as np, rosbag, tf.transformations as tr
DESC = 'Combine multiple topics from different bags in one bag'




def get_from_bag(input_bag_file1, input_bag_file2, topicss, out='out.bag'):
    with rosbag.Bag(out, 'w') as outbag:
        for topic, msg, t in rosbag.Bag(input_bag_file1).read_messages(topics=topicss):
            if topic in topicss:
                outbag.write(topic, msg, t)
        # print("Done bag1")
        for topic, msg, t in rosbag.Bag(input_bag_file2).read_messages(topics=topicss):
            if topic in topicss:
                outbag.write(topic, msg, t)
        # print("Done bag2")




if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument('input_bag_file1', help='input bag1 path file')
    parser.add_argument('input_bag_file2', help='input bag2s path file')
    parser.add_argument('out', help='output bag file path')
    parser.add_argument('topics', nargs='+', help='topic for which to create a TUM file')

    args = parser.parse_args()
    get_from_bag(args.input_bag_file1, args.input_bag_file2, args.topics, args.out)