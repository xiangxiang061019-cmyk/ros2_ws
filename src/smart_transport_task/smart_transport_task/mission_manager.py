import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from smart_transport_interfaces.msg import TaskOrder

from .task_code import parse_task_code


class MissionManager(Node):
    def __init__(self):
        super().__init__('mission_manager')
        self.state_publisher = self.create_publisher(String, '/mission/state', 10)
        self.order_publisher = self.create_publisher(TaskOrder, '/mission/order', 10)
        self.subscription = self.create_subscription(
            String, '/qr/task_code', self.on_task_code, 10)
        self.publish_state('INIT')
        self.get_logger().info('Mission manager ready; waiting for /qr/task_code.')

    def publish_state(self, state):
        msg = String()
        msg.data = state
        self.state_publisher.publish(msg)

    def on_task_code(self, msg):
        self.publish_state('READ_TASK')
        order = TaskOrder()
        order.header.stamp = self.get_clock().now().to_msg()
        order.raw_code = msg.data.strip()
        try:
            parsed = parse_task_code(order.raw_code)
        except ValueError as exc:
            order.valid = False
            order.error = str(exc)
            self.order_publisher.publish(order)
            self.publish_state('READ_TASK_ERROR')
            self.get_logger().warning(f'invalid task code: {exc}')
            return

        order.first_colors = parsed['first_colors']
        order.first_places = parsed['first_places']
        order.second_colors = parsed['second_colors']
        order.second_places = parsed['second_places']
        order.valid = True
        order.error = ''
        self.order_publisher.publish(order)
        self.publish_state('TASK_READY')
        self.get_logger().info(f'accepted task code: {order.raw_code}')


def main(args=None):
    rclpy.init(args=args)
    node = MissionManager()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
