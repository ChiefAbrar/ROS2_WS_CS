import rclpy, math
from rclpy.node import Node
from geometry_msgs.msg import Vector3

L1 = 14.0
L2 = 15.5

class FKNode(Node):
    def __init__(self):
        super().__init__('forward_kinematics')
        self.create_subscription(Vector3, '/miniarm/angles', self.cb, 10)

    def cb(self, msg: Vector3):
        theta1 = math.radians(msg.x)
        theta2 = math.radians(180.0 - msg.y)

        x1 = L1 * math.cos(theta1)
        y1 = L1 * math.sin(theta1)

        x2 = x1 + L2 * math.cos(theta1 + theta2)
        y2 = y1 + L2 * math.sin(theta1 + theta2)

        self.get_logger().info(f"Forward Kinematics → x = {x2:.2f}, y = {y2:.2f}")

def main():
    rclpy.init()
    rclpy.spin(FKNode())
    rclpy.shutdown()

if __name__ == '__main__':
    main()
