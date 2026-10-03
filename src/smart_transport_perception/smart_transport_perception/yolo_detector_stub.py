import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class YoloDetectorStub(Node):
    def __init__(self):
        super().__init__('yolo_detector')
        self.declare_parameter('camera_topic', '/grasp_camera/image_raw')
        self.declare_parameter('model_path', '')
        self.publisher = self.create_publisher(String, '/perception/yolo/status', 10)
        self.timer = self.create_timer(1.0, self.publish_status)
        self.get_logger().info('YOLO detector placeholder started; no model is loaded.')

    def publish_status(self):
        msg = String()
        model = str(self.get_parameter('model_path').value) or '<unset>'
        msg.data = 'waiting_for_yolo model=' + model
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = YoloDetectorStub()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
