
import os
# for i in range(11):
#     cmd = "python ../scripts/create_bag_from_topics.py ../visual_odom/seq_{}.bag ../bag_0_{}/bag/bag.bag seq_{}.bag /odom /kitti/oxts/imu".format(i,i,i)
#     print("Creating bag {}".format(i))
#     os.system(cmd)


for i in range(1):
    if i == 3:
        continue
    cmd = "python ../scripts/reset_time.py ../visual_odom/seq_{}.bag ../bag_0_{}/bag/bag.bag /kitti/oxts/imu".format(i,i)
    os.system(cmd)

    # Copying
    # cmd = "cp t_seq_{}.bag ../bag_0_{}/bag/seq_{}.bag".format(i,i,i)
    # print("Copying bag {}".format(i))
    # os.system(cmd)

