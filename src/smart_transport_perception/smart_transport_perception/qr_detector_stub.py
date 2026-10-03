import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class QrDetectorStub(Node):
    def __init__(self):
        super().__init__('qr_detector')
        self.declare_parameter('camera_topic', '/qr_camera/image_raw')
        self.publisher = self.create_publisher(String, '/perception/qr/status', 10)
        self.timer = self.create_timer(1.0, self.publish_status)
        self.get_logger().info('QR detector placeholder started; no camera driver is connected.')

    def publish_status(self):
        msg = String()
        msg.data = 'waiting_for_qr_detector camera_topic=' + str(
            self.get_parameter('camera_topic').value)
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = QrDetectorStub()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
