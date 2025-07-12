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
        theta1_deg = msg.x
        theta2_deg = msg.y

        # Convert to radians
        theta1 = math.radians(theta1_deg)
        # Use relative elbow rotation:
        theta2 = math.radians(180.0 - theta2_deg)

        # Compute end-effector position
        x = L1 * math.cos(theta1) + L2 * math.cos(theta1 - theta2)
        y = L1 * math.sin(theta1) + L2 * math.sin(theta1 - theta2)

        self.get_logger().info(
            f"Received: θ1={theta1_deg:.2f}°, θ2={theta2_deg:.2f}° → FK: x={x:.2f}, y={y:.2f}"
        )

def main():
    rclpy.init()
    rclpy.spin(FKNode())
    rclpy.shutdown()

if __name__ == '__main__':
    main()
