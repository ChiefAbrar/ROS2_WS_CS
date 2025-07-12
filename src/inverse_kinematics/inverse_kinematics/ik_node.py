import rclpy, math
from rclpy.node import Node
from geometry_msgs.msg import Vector3

L1 = 14.0
L2 = 15.5

class IKNode(Node):
    def __init__(self):
        super().__init__('inverse_kinematics')
        self.create_subscription(Vector3, '/miniarm/target', self.cb, 10)
        self.pub = self.create_publisher(Vector3, '/miniarm/angles', 10)

    def cb(self, msg:Vector3):
        x, y = msg.x, msg.y
        d = math.hypot(x, y)
        if d > L1+L2 or d < abs(L1-L2):
            self.get_logger().error("Target out of reach")
            return
        try:
            cos_phi = (L1**2 + L2**2 - d**2)/(2*L1*L2)
            phi = math.acos(cos_phi)
            theta2 = math.degrees(math.pi - phi)  # 180°-φ

            cos_beta = (L1**2 + d**2 - L2**2)/(2*L1*d)
            beta = math.acos(cos_beta)
            alpha = math.atan2(y, x)
            theta1 = math.degrees(alpha + beta)

            theta1 = max(0, min(180, theta1))
            theta2 = max(0, min(180, theta2))

            out = Vector3()
            out.x = float(theta1)
            out.y = float(theta2)
            out.z = 0.0
            self.pub.publish(out)
            self.get_logger().info(f"θ1={theta1:.1f}°, θ2={theta2:.1f}°")
        except ValueError:
            self.get_logger().error("Math domain error – check inputs")

def main():
    rclpy.init()
    rclpy.spin(IKNode())
    rclpy.shutdown()
if __name__ == '__main__': main()