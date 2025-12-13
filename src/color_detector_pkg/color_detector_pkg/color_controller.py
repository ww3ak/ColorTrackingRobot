import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist


class ColorController(Node):


   def __init__(self):
       super().__init__('color_controller')


       self.declare_parameter('max_linear_speed', 0.5)
       self.declare_parameter('angular_gain', 0.0025)
       self.declare_parameter('stop_if_no_color', True)
       self.declare_parameter('cmd_topic', '/cmd_vel')
       self.declare_parameter('color_topic', '/color_detected')


       self.linear_speed= self.get_parameter('max_linear_speed').value
       self.angular_gain = self.get_parameter('angular_gain').value
       self.cmd_topic = self.get_parameter('cmd_topic').value
       self.color_topic = self.get_parameter('color_topic').value


       self.current_color = None


       self.map = {
           'blue': (-self.linear_speed, -self.angular_gain),
           'green': (-self.linear_speed, self.angular_gain),
           'yellow': (self.linear_speed, -self.angular_gain),
           'red': (self.linear_speed, self.angular_gain)
       }


       self.pub = self.create_publisher(Twist, self.cmd_topic, 10)
       self.sub = self.create_subscription(String, '/color_detected', self.color_callback, 10)


       self.get_logger().info(f'color_controller started. Waiting on: {self.color_topic}')


   def color_callback(self, msg: String):
       color = msg.data.strip().lower()
       if color in self.map:
           self.current_color = color
           self.get_logger().info(f'Color: {color}')
       else:
           self.current_color = None
      
   def publish_move(self):
       twist = Twist()
       if self.current_color is None:
           twist.linear.x = 0.0
           twist.linear.z = 0.0
       else:
           lin, ang = self.map[self.current_color]
           twist.linear.x = lin
           twist.angular.z = ang
       self.pub.publish(twist)


def main(args=None):
    rclpy.init(args=args)
    node = ColorController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
