# Smart Transport ROS 2 Workspace

This workspace is the initial ROS 2 skeleton for the intelligent transport
robot. Package names are ASCII so the same source can be built on the R1
Ubuntu 22 / ROS 2 Humble system and the development Ubuntu 24 / ROS 2 Jazzy
system.

## Packages

- `smart_transport_interfaces`: shared task and detection messages.
- `smart_transport_description`: minimal robot model and sensor frame names.
- `smart_transport_bringup`: one launch entry point and external map loading.
- `smart_transport_hardware`: OPS9 and 02Lower protocol placeholders.
- `smart_transport_perception`: QR, YOLO and LiDAR placeholder nodes.
- `smart_transport_task`: task-code parser and initial mission state.

The hardware and perception nodes deliberately do not publish fake odometry,
fake detections, or fake obstacle data. The real serial protocols, camera
drivers and radar driver can be added without changing the launch structure.

## Build on the development computer

```bash
cd /home/xiaoyu/ros2_ws
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install
source install/setup.bash
ros2 launch smart_transport_bringup competition.launch.py
```

On the R1, source the installed Humble environment instead. Nav2 and the map
server are optional in the initial launch because they are not installed on
the development image yet.

To enable the map after installing Nav2:

```bash
ros2 launch smart_transport_bringup competition.launch.py \
  use_map:=true \
  map_yaml:=/home/xiaoyu/map/competition_nominal.yaml
```

The nominal map remains an external planning input. Runtime object positions
should be published as detections and costmap observations; they should not be
written back into the PGM file.
