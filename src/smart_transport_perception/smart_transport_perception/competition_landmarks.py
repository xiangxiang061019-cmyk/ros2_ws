from geometry_msgs.msg import Point
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile, ReliabilityPolicy
import rclpy
from visualization_msgs.msg import Marker, MarkerArray


class CompetitionLandmarks(Node):
    """Publish nominal competition regions as an RViz overlay."""

    def __init__(self):
        super().__init__('competition_landmarks')
        self.declare_parameter('frame_id', 'map')
        qos = QoSProfile(depth=1)
        qos.durability = DurabilityPolicy.TRANSIENT_LOCAL
        qos.reliability = ReliabilityPolicy.RELIABLE
        self.publisher = self.create_publisher(
            MarkerArray, '/competition_landmarks', qos)
        self.publish_markers()
        self.get_logger().info(
            'Publishing nominal competition regions on /competition_landmarks')

    def marker(self, marker_id, marker_type, namespace):
        marker = Marker()
        marker.header.frame_id = str(self.get_parameter('frame_id').value)
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = namespace
        marker.id = marker_id
        marker.type = marker_type
        marker.action = Marker.ADD
        marker.pose.orientation.w = 1.0
        marker.color.a = 1.0
        return marker

    @staticmethod
    def set_color(marker, red, green, blue, alpha=1.0):
        marker.color.r = red
        marker.color.g = green
        marker.color.b = blue
        marker.color.a = alpha

    @staticmethod
    def set_center(marker, x, y, z=0.02):
        marker.pose.position.x = x
        marker.pose.position.y = y
        marker.pose.position.z = z

    @staticmethod
    def add_rectangle(marker, x0, y0, x1, y1, z=0.03):
        marker.points = [
            Point(x=x0, y=y0, z=z),
            Point(x=x1, y=y0, z=z),
            Point(x=x1, y=y1, z=z),
            Point(x=x0, y=y1, z=z),
            Point(x=x0, y=y0, z=z),
        ]

    def add_label(self, markers, marker_id, text, x, y, color):
        label = self.marker(marker_id, Marker.TEXT_VIEW_FACING, 'labels')
        label.text = text
        label.scale.z = 0.05
        self.set_center(label, x, y, 0.12)
        self.set_color(label, *color)
        label.frame_locked = True
        markers.markers.append(label)

    def publish_markers(self):
        markers = MarkerArray()

        for marker_id, x, y, text in [
            (1, 2.25, 2.25, 'S1'),
            (2, 2.25, 0.15, 'S2'),
        ]:
            zone = self.marker(marker_id, Marker.CUBE, 'start_stop_zones')
            zone.scale.x = 0.30
            zone.scale.y = 0.30
            zone.scale.z = 0.01
            self.set_center(zone, x, y, 0.01)
            self.set_color(zone, 0.05, 0.25, 1.0, 0.42)
            markers.markers.append(zone)
            self.add_label(markers, marker_id, text, x, y, (0.05, 0.25, 1.0))

        for marker_id, bounds, text, color in [
            (1, (0.0, 0.91, 0.15, 1.49), 'TEMP', (0.95, 0.55, 0.05)),
            (2, (0.91, 0.0, 1.49, 0.15), 'ROUGH', (0.95, 0.55, 0.05)),
        ]:
            outline = self.marker(marker_id, Marker.LINE_STRIP, 'work_zones')
            outline.scale.x = 0.015
            self.add_rectangle(outline, *bounds)
            self.set_color(outline, *color)
            markers.markers.append(outline)
            x0, y0, x1, y1 = bounds
            self.add_label(markers, marker_id + 10, text,
                           (x0 + x1) / 2.0, (y0 + y1) / 2.0, color)

        raw = self.marker(1, Marker.LINE_STRIP, 'search_regions')
        raw.scale.x = 0.012
        self.add_rectangle(raw, 0.95, 2.315, 1.45, 2.40)
        self.set_color(raw, 1.0, 0.35, 0.02)
        markers.markers.append(raw)
        self.add_label(markers, 20, 'RAW', 1.20, 2.34,
                       (1.0, 0.35, 0.02))

        qr = self.marker(2, Marker.LINE_STRIP, 'search_regions')
        qr.scale.x = 0.012
        qr.points = [
            Point(x=2.395, y=1.10, z=0.03),
            Point(x=2.395, y=1.30, z=0.03),
        ]
        self.set_color(qr, 0.0, 0.75, 0.55)
        markers.markers.append(qr)
        self.add_label(markers, 21, 'QR', 2.30, 1.20,
                       (0.0, 0.75, 0.55))

        self.publisher.publish(markers)


def main(args=None):
    rclpy.init(args=args)
    node = CompetitionLandmarks()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
