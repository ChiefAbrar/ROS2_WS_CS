import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64, Float64, String as StringMsg
import serial

class SerialNode(Node):
    def __init__(self):
        super().__init__('serial_node')

        # Serial port (adjust it accordingly written in the documentation)
        self.ser = serial.Serial('/dev/pts/10', 115200, timeout=1)

        self.pub_a = self.create_publisher(Int64, '/sensor_data/value_a', 10)
        self.pub_b = self.create_publisher(Float64, '/sensor_data/value_b', 10)
        self.pub_c = self.create_publisher(Int64, '/sensor_data/value_c', 10)
        self.pub_d = self.create_publisher(StringMsg, '/sensor_data/value_d', 10)

        self.subscription = self.create_subscription(
            StringMsg, 'led_control', self.send_command_to_arduino, 10)

        self.timer = self.create_timer(1.0, self.read_serial)

    def send_command_to_arduino(self, msg):
        command = msg.data.strip()
        self.ser.write((command + '\n').encode())
        self.get_logger().info(f"Sent to Arduino: {command}")

    def read_serial(self):
        if self.ser.in_waiting:
            line = self.ser.readline().decode().strip()
            parts = line.split(',')
            if len(parts) == 4:
                try:
                    value_a = int(parts[0])
                    value_b = float(parts[1])
                    value_c = int(parts[2])
                    value_d = parts[3]

                    self.pub_a.publish(Int64(data=value_a))
                    self.pub_b.publish(Float64(data=value_b))
                    self.pub_c.publish(Int64(data=value_c))
                    self.pub_d.publish(StringMsg(data=value_d))

                    self.get_logger().info(f"Sensor A: {value_a}, B: {value_b}, C: {value_c}, D: {value_d}")
                except ValueError:
                    self.get_logger().warn("Received malformed data.")

def main(args=None):
    rclpy.init(args=args)
    node = SerialNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()
