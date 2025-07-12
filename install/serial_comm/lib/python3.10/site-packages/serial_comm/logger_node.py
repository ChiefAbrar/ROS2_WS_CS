import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64, Float64, String

class LoggerNode(Node):
    def __init__(self):
        super().__init__('logger_node')

        self.create_subscription(Int64, '/sensor_data/value_a', self.cb_a, 10)
        self.create_subscription(Float64, '/sensor_data/value_b', self.cb_b, 10)
        self.create_subscription(Int64, '/sensor_data/value_c', self.cb_c, 10)
        self.create_subscription(String, '/sensor_data/value_d', self.cb_d, 10)

    def cb_a(self, msg): self.get_logger().info(f"Value A: {msg.data}")
    def cb_b(self, msg): self.get_logger().info(f"Value B: {msg.data:.2f}")
    def cb_c(self, msg): self.get_logger().info(f"Value C: {msg.data}")
    def cb_d(self, msg): self.get_logger().info(f"Value D: {msg.data}")

def main():
    rclpy.init()
    rclpy.spin(LoggerNode())
    rclpy.shutdown()

if __name__ == '__main__':
    main()
