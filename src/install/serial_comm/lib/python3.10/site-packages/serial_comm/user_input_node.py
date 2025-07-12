import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class UserInputNode(Node):
    def __init__(self):
        super().__init__('user_input_node')
        self.publisher_ = self.create_publisher(String, 'led_control', 10)
        self.timer = self.create_timer(2.0, self.get_user_input)

    def get_user_input(self):
        cmd = input("Enter LED command (ON/OFF): ")
        msg = String()
        msg.data = cmd.strip().upper()
        self.publisher_.publish(msg)
        self.get_logger().info(f"Sent command: {msg.data}")

def main(args=None):
    rclpy.init(args=args)
    node = UserInputNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()
