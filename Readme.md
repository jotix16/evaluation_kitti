# Evaluation of robot_localization and localization_fusion_library on kitti dataset


``` bash
pip install evo
sudo apt install ros-melodic-rtabmap-ros
sudo apt install ros-melodic-robot-localization

mkdir -p ~/eval_ws/src
cd ~/eval_ws/src
git clone [...]Localization_Fusion_Library.git
git clone https://github.com/jotix16/evaluation_kitti.git
cd ~/eval_ws
catkin_make

```

## Run evaluation for seq_4

``` bash

cd ~/eval_ws/src/evaluation_kitti/eval/bag_0_4/
# make sure to outcomment the lines where the dataset gets downloaded
./run_eval.sh
```

