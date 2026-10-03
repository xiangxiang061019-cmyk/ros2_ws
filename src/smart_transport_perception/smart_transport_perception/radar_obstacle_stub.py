import math

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String


class RadarObstacleStub(Node):
    def __init__(self):
        super().__init__('radar_obstacle')
        self.declare_parameter('scan_topic', '/scan')
        self.publisher = self.create_publisher(String, '/perception/radar/status', 10)
        self.subscription = self.create_subscription(
            LaserScan,
            self.get_parameter('scan_topic').value,
            self.on_scan,
            10,
        )
        self.min_range = None
        self.timer = self.create_timer(1.0, self.publish_status)
        self.get_logger().info('Radar placeholder started; obstacle classification is pending.')

    def on_scan(self, scan):
        valid = [value for value in scan.ranges if math.isfinite(value)]
        self.min_range = min(valid) if valid else None

    def publish_status(self):
        msg = String()
        if self.min_range is None:
            msg.data = 'waiting_for_scan topic=' + str(self.get_parameter('scan_topic').value)
        else:
            msg.data = f'scan_received min_range_m={self.min_range:.3f}'
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = RadarObstacleStub()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
