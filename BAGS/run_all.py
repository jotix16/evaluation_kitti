import os

# for i in range(11):
#     cmd = "python ../scripts/create_bag_from_topics.py ../visual_odom/seq_{}.bag ../bag_0_{}/bag/bag.bag seq_{}.bag /odom /kitti/oxts/imu".format(i,i,i)
#     print("Creating bag {}".format(i))
#     os.system(cmd)


for i in range(11):
    cmd = "cp seq_{}.bag ../bag_0_{}/bag".format(i,i)
    print("Copying bag {}".format(i))
    os.system(cmd)