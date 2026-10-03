from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class LowerDriver(Node):
    def __init__(self):
        super().__init__('lower_driver')
        self.declare_parameter('enabled', False)
        self.declare_parameter('port', '/dev/ttyUSB1')
        self.declare_parameter('baudrate', 115200)
        self.declare_parameter('dry_run', True)
        self.latest_cmd = Twist()
        self.received_cmd = False
        self.publisher = self.create_publisher(String, '/hardware/lower/status', 10)
        self.subscription = self.create_subscription(Twist, '/cmd_vel', self.on_cmd_vel, 10)
        self.timer = self.create_timer(1.0, self.publish_status)
        self.get_logger().info(
            '02Lower driver placeholder started; A5 5A protocol is not implemented yet.')

    def on_cmd_vel(self, msg):
        self.latest_cmd = msg
        self.received_cmd = True

    def publish_status(self):
        msg = String()
        if not self.received_cmd:
            msg.data = 'waiting_for_cmd_vel'
        else:
            msg.data = (
                f'cmd_vel vx={self.latest_cmd.linear.x:.3f} '
                f'vy={self.latest_cmd.linear.y:.3f} '
                f'wz={self.latest_cmd.angular.z:.3f}'
            )
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = LowerDriver()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
