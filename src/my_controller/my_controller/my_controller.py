import rclpy
import tf_transformations
from rclpy.node import Node                                                                             
from std_msgs.msg import String                                                                         
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import PoseWithCovarianceStamped
from nav_msgs.msg import Odometry
from tf_transformations import euler_from_quaternion

class ControlNode(Node):                                                                               
    def __init__(self):
        super().__init__('amcl_subscriber_node')                                                          
        self.create_subscription(PoseWithCovarianceStamped, 'amcl_pose', self.amcl_cb, 10)                  
        self.create_subscription(Odometry,'odom',self.odom_cb, 10)   

    def control(self):
        #input: position, velosity
        posx = 0
        posy = 0
        speedt = 0
        speedr = 0

        #MPPI

        #output: speed of each wheel
        #temporary output: transition speed, rotation speed
        return speedt, speedr

    def MPPI(self):
        u = 0
    
    def StateEquation(self):
        x = 0

    def CostFunction(self):
        cost = 0
    
    def StageCost(self):
        cost = 0

    def TerminalCost(self):
        terminalcost = 0

def main():
    print('Hi from my_controller.')


if __name__ == '__main__':
    main()
