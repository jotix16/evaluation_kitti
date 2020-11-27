import rosbag

    
# rob_bag = rosbag.Bag('bag/rob_lib.bag', 'w')
# loc_bag = rosbag.Bag('bag/loc_lib.bag', 'w')
rob_bag = 'bag/rob_lib.bag'
loc_bag = 'bag/loc_lib.bag'

    # with rosbag.Bag('bag/rob_lib.bag', 'w') as rob_bag, rosbag.Bag('bag/loc_lib.bag', 'w') as loc_bag:
a = 0
pr = []
for topic, msg, t in rosbag.Bag(rob_bag).read_messages():
    if topic == '/odometry/filtered_rob':
        # print("rob_lib", t)
        pr.append(t.to_sec())
        a +=1
        if a == 3:
            break
    else:
        pass

a = 0
pr2 = []
for topic, msg, t in rosbag.Bag(loc_bag).read_messages():
    if topic == '/odometry/filtered':
        pr2.append(t.to_sec())
        a +=1
        # print("loc_lib", t)
        if a == 3:
            break
    else:
        pass

print(rosbag.Bag(rob_bag).get_start_time()- rosbag.Bag(loc_bag).get_start_time())
print([a-b for a,b in zip(pr, pr2)])
print(pr)
print(pr2)