#!/usr/bin/env python

# ROS dependencies
import rospy
from std_msgs.msg import String
from nxt_msgs.msg import Light
from geometry_msgs.msg import Twist



# geometry_msgs/Twist
# nxt_msgs/Light

light_l = 0.0
light_r = 0.0

# Callbacks
def callback_light_l(data):
    global light_l
    light_l = data.intensity

def callback_light_r(data):
    global light_r
    light_r = data.intensity

def calibracao():
    # obtem os valores para branco e preto de cada sensor
    raw_input("\nPosicione o robo com os dois sensores na pista branca e digite enter...")
    white_l = light_l
    white_r = light_r
    print "\nWhiteLeft = " + str(white_l)
    print "WhiteRight = " + str(white_r)

    raw_input("\nPosicione o robo com o sensor numero 4 sobre a cor preta e digite enter...")
    black_r = light_r
    print"\nBlackRight = " + str(black_r)

    raw_input("\nPosicione o robo com o sensor numero 8 sobre a cor preta e digite enter...")
    black_l = light_l
    print"\nBlackLeft = " + str(black_l)

    # trata os dados recebidos
    print "\n\nTratando os dados recebidos..."
    
    light_tresh_l = (white_l + black_l) / 2
    light_tresh_r = (white_r + black_r) / 2

    return light_tresh_l, light_tresh_r;

def line_follower(light_tresh_l, light_tresh_r):
    # initial config
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    # set manual threshold
    #light_tresh_r = 430.0
    #light_tresh_l = 400.0

    black_l = 400.0
    black_r = 400.0

    vel_msg = Twist()
    vel_msg.linear.x = 0
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0

    # angular = rad/s
    # linear = m/s

    rate = rospy.Rate(100)  # original = 10 Hz  

    while not rospy.is_shutdown():
        if light_l < light_tresh_l:               # carrinho indo para direita
            vel_msg.linear.x = 0.03
            vel_msg.angular.z = 0.25
        elif light_r < light_tresh_r:             # carrinho indo para esquerda
            vel_msg.linear.x = 0.03
            vel_msg.angular.z = -0.25
        else:
            vel_msg.linear.x = 0.04
            vel_msg.angular.z = 0.0

        pub.publish(vel_msg)
        rate.sleep()

if __name__ == '__main__':
    # initial config
    light_tresh_l = 562
    light_tresh_r = 578

    rospy.init_node('light_control', anonymous=True)
    
    rospy.Subscriber("/light_l", Light, callback_light_l)
    rospy.Subscriber("/light_r", Light, callback_light_r)
 
    choose = raw_input("Digite\n\r\t0 - Calibracao\n\r\t1 - Seguidor de linha\n")

    if choose == "0":
        light_tresh_l, light_tresh_r = calibracao()
        line_follower(light_tresh_l, light_tresh_r)
    else:
        line_follower(light_tresh_l, light_tresh_r)

