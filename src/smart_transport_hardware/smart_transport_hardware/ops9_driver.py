import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Ops9Driver(Node):
    def __init__(self):
        super().__init__('ops9_driver')
        self.declare_parameter('enabled', False)
        self.declare_parameter('port', '/dev/ttyUSB0')
        self.declare_parameter('baudrate', 115200)
        self.publisher = self.create_publisher(String, '/hardware/ops9/status', 10)
        self.timer = self.create_timer(1.0, self.publish_status)
        self.get_logger().info(
            'OPS9 driver placeholder started; parser and encoder configuration are pending.')

    def publish_status(self):
        msg = String()
        enabled = bool(self.get_parameter('enabled').value)
        port = str(self.get_parameter('port').value)
        msg.data = ('serial_parser_pending' if enabled else 'disabled') + ' port=' + port
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = Ops9Driver()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
