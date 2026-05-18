import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
import tf2_ros
from geometry_msgs.msg import TransformStamped
import sys
import select
import tty
import termios
import threading
import time
import math

class KeyboardController(Node):

    def __init__(self):
        super().__init__('keyboard_controller')
        self.publisher_ = self.create_publisher(JointState, 'joint_states', 10)



        self.tf_broadcaster = tf2_ros.TransformBroadcaster(self)
        self.settings = termios.tcgetattr(sys.stdin)
        self.angle = 0.0
        self.speed = 0.1
        self.running = True
        self.auto_rotate = 0  # 0: not rotating, 1: clockwise, -1: counterclockwise
        self.get_logger().info('Use WASD keys to control the wheel. Press Q to quit.')
        self.thread = threading.Thread(target=self.update_joint_state)
        self.thread.start()


    def read_key(self):
        tty.setraw(sys.stdin.fileno())
        select.select([sys.stdin], [], [], 0)
        key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
        return key

    def update_joint_state(self):
        while self.running:
            if self.auto_rotate == 1:
                self.angle += self.speed
            elif self.auto_rotate == -1:
                self.angle -= self.speed

            joint_state = JointState()
            joint_state.header = Header()
            joint_state.header.stamp = self.get_clock().now().to_msg()
            joint_state.name = ['base_to_wheel']
            joint_state.position = [self.angle]
            self.publisher_.publish(joint_state)

            t = TransformStamped()
            t.header.stamp = self.get_clock().now().to_msg()
            t.header.frame_id = 'base_link'
            t.child_frame_id = 'wheel_link'
            t.transform.translation.x = 0.0
            t.transform.translation.y = 0.0
            t.transform.translation.z = 0.0
            q = self.angle_to_quaternion(self.angle)
            t.transform.rotation.x = q[0]
            t.transform.rotation.y = q[1]
            t.transform.rotation.z = q[2]
            t.transform.rotation.w = q[3]

            self.tf_broadcaster.sendTransform(t)
            time.sleep(0.1)

    def angle_to_quaternion(self, angle):
        qx = 0.0
        qy = 0.0
        qz = math.sin(angle / 2)
        qw = math.cos(angle / 2)
        return (qx, qy, qz, qw)

    def run(self):
        try:
            while True:
                key = self.read_key()
                if key == 'w':
                    self.speed += 0.1
                elif key == 's':
                    self.speed -= 0.1
                elif key == 'a':
                    self.auto_rotate = 1  
                elif key == 'd':
                    self.auto_rotate = -1  
                elif key == 'q':
                    self.running = False
                    break
                else:
                    continue

                self.get_logger().info(f'Updated: angle={self.angle}, speed={self.speed}, auto_rotate={self.auto_rotate}')

        except Exception as e:
            self.get_logger().error(f'Error: {e}')
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)

def main(args=None):
    rclpy.init(args=args)
    node = KeyboardController()
    try:
        node.run()
    except KeyboardInterrupt:
        pass
    finally:
        node.running = False
        node.thread.join()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

















