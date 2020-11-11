import numpy as np
file = open('00.txt', 'r')
Lines = file.readline()
T_cam0_cam = np.array(Lines.split(), dtype=np.float).reshape(3,4)


print(T_cam0_cam)
print(T_cam0_cam.shape)


print(file.closed)
file.close()
print(file.closed)