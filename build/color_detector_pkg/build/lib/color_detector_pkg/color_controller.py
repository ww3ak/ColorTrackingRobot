import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import TwistStamped


class ColorController(Node):

    def __init__(self):
        super().__init__('color_controller')

        self.declare_parameter('max_linear_speed', 0.2)
        self.declare_parameter('angular_gain', 0.4)
        self.declare_parameter('turn_time', 1.0)
        self.declare_parameter('run_time', 50.0)
        self.declare_parameter('cmd_topic', '/cmd_vel')
        self.declare_parameter('color_topic', '/color_detected')

        self.run_time = self.get_parameter('run_time').value
        self.turn_time = self.get_parameter('turn_time').value
        self.linear_speed = self.get_parameter('max_linear_speed').value
        self.angular_gain = self.get_parameter('angular_gain').value
        self.cmd_topic = self.get_parameter('cmd_topic').value
        self.color_topic = self.get_parameter('color_topic').value
        
        self.time_start = self.get_clock().now()
        self.current_color = None
        self.last_color = None
        self.turn_end_time = 0.0

        self.map = {
            'blue': (-self.linear_speed, self.angular_gain),
            'green': (-self.linear_speed, -self.angular_gain),
            'yellow': (self.linear_speed, -self.angular_gain),
            'red': (self.linear_speed, self.angular_gain)
        }

        self.pub = self.create_publisher(TwistStamped, self.cmd_topic, 10)
        self.sub = self.create_subscription(String, self.color_topic, self.color_callback, 10)

        self.timer = self.create_timer(0.1, self.publish_move)

        self.get_logger().info(f'=== COLOR CONTROLLER STARTED ===')
        self.get_logger().info(f'Subscribing to: {self.color_topic}')
        self.get_logger().info(f'Publishing to: {self.cmd_topic}')
        self.get_logger().info(f'Linear speed: {self.linear_speed}')
        self.get_logger().info(f'Angular gain: {self.angular_gain}')

    def color_callback(self, msg: String):
        color = msg.data.strip().lower()
        #self.get_logger().info(f'>>> Received color: "{color}"')
        if color in self.map and color != self.last_color:
            self.current_color = color
            self.last_color = color
            self.turn_end_time = (self.get_clock().now().nanoseconds/1e9 + self.turn_time)
            self.get_logger().info(f'>>> Valid color set: {color}')
        elif color not in self.map:
            self.get_logger().warn(f'>>> Unknown color: {color}')
            self.current_color = None
    
    def publish_move(self):
        twist_stamped = TwistStamped()
        twist_stamped.header.stamp = self.get_clock().now().to_msg()
        twist_stamped.header.frame_id = "base_link"

        current_time = self.get_clock().now().nanoseconds/1e9
        delta = (self.get_clock().now() - self.time_start).nanoseconds/1e9

        if delta >= self.run_time:
            twist_stamped.twist.linear.x = 0.0
            twist_stamped.twist.angular.z = 0.0
            self.pub.publish(twist_stamped)
            return
        
        if self.current_color is None:
            twist_stamped.twist.linear.x = 0.0
            twist_stamped.twist.angular.z = 0.0
        else:
            lin, ang = self.map[self.current_color]
            if current_time < self.turn_end_time:
                twist_stamped.twist.linear.x = 0.0
                twist_stamped.twist.angular.z = ang
            else:
                twist_stamped.twist.linear.x = lin
                twist_stamped.twist.angular.z = 0.0
            self.get_logger().info(f'>>> PUBLISHING MOVEMENT: linear={lin}, angular={ang}')
        
        self.pub.publish(twist_stamped)


def main(args=None):
    rclpy.init(args=args)
    node = ColorController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()