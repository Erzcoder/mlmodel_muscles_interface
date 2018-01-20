#!/usr/bin/env python
# license removed for brevity

'''
@author Nicolas Berberich, Werner Seitz, Pranshul Saini, Steffen Schneider
@date   20.01.2018



'''

import rospy

from roboy_communication_middleware.msg import MotorCommand
import numpy as np
from geometry_msgs.msg import Point


'''
Point
float64 x
float64 y
float64 z
'''

'''
MotorCommand
uint8[] motors
int32[] setPoints
'''


# TODO: should also subscribe to the joint angle to take care of the joint limit


def talker():
    rospy.init_node('move_to_3dpos')
    rate = rospy.Rate(10) # 10hz
    rospy.Subscriber('/desired_EFposition', Point, callback)
    rospy.spin()

def mlmodel(readout_rates):
    # take care of joint and motor limits
    motor_commands = []
    for rate in readout_rates:
        motor_commands.append(rate/100.)

    return motor_commands
    

def callback(data_input):

    motor_commands = MotorCommand()
    desired_EFposition = data_input

    motor_commands.motors = [5,6] # predefine which motors to use
    
    
    motor_commands.setPoints = mlmodel(desired_EFposition)
    pub = rospy.Publisher('/motor_commands', MotorCommand, queue_size=10) 
    
    print motor_commands
    pub.publish(motor_commands)

	

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass