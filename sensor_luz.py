#! /usr/bin/env python

# ROS dependencies
import rospy
from std_msgs.msg import String
from nxt_msgs.msg import Light              # nxt_msgs/Light
from geometry_msgs.msg import Twist         # geometry_msgs/Twist

# Other dependencies
import sys
import auxiliar

# variables of limits black-white
black_l = 0
black_r = 0
white_l = 0
white_r = 0

#threshold after remap
threshold_light = 50

# Standard Callbacks
def callback_light_l(data):
    global light_l
    value = data.intensity
    light_l = auxiliar.remap(value, black_l, white_l, 0, 100)

def callback_light_r(data):
    global light_r
    value = data.intensity
    light_r = auxiliar.remap(value, black_r, white_l, 0, 100)

# Callbacks for calibration
def callback_calib_l(data):
    global light_l
    light_l = data.intensity

def callback_calib_l(data):
    global light_r
    light_r = data.intensity

# calibration routine
def calibration():
    print "Iniciando calibracao"

    # obtem os valores para branco e preto de cada sensor
    raw_input("\nPosicione o robo com os sensores sobre o branco e digite enter...")
    white_l = light_l
    white_r = light_r
    print "\nWhiteLeft = " + str(white_l)
    print "WhiteRight = " + str(white_r)

    raw_input("\nPosicione o robo com os sensores sobre o preto e digite enter...")
    black_r = light_r
    black_l = light_l
    print"\nBlackLeft = " + str(black_l)
    print"BlackRight = " + str(black_r)
    
    # com remap 0-100 sendo executado é possivel manter o threshold estável em 50 
    print "\n\nDados armazenados para remap dos sensores"

def line_follower(light_tresh_l, light_tresh_r):
    # initial config
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    vel_msg = Twist()
    vel_msg.linear.x = 0
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0

    # angular = rad/s
    # linear = m/s

    rate = rospy.Rate(20)  # original = 10 Hz  

    while not rospy.is_shutdown():              # principal loop
        light_error = light_l - light_r

        # proportional control
        kp_linear = 0.0
        kp_angular = 0.0

        vel_msg.linear.x = 0.04 - (kp_linear * light_error)     # where kp * error can be up to 0.02 (max value for do not stop the car)
                                                                # 0.04 is an acceptable value for the velocity of the car
        vel_msg.angular.z = kp_angular * light_error            # kp * error, in this case, can be up to 0.25 with the experimental tests
        
        pub.publish(vel_msg)
        rate.sleep()

def main():
    # Initial config
    light_tresh_l = 562
    light_tresh_r = 578

    rospy.init_node('light_control', anonymous=True)        # pra que??
    
    # Parser of calibration arg
    if len(sys.argv) > 1:
        # select the callbacks for the calibration
        sensor_l = rospy.Subscriber("/light_l", Light, callback_calib_l)
        sensor_r rospy.Subscriber("/light_r", Light, callback_calib_r)

        globals()[sys.argv[1]]()

        sensor_l.unregister()
        sensor_r.unregister)()

    # Line follower 
    rospy.Subscriber("/light_l", Light, callback_light_l)
    rospy.Subscriber("/light_r", Light, callback_light_r)

    line_follower(light_tresh_l, light_tresh_r)

if __name__ == '__main__':
    main()