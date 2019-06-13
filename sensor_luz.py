#! /usr/bin/env python

# ROS dependencies
import rospy
from std_msgs.msg import String
from nxt_msgs.msg import Light              # nxt_msgs/Light
from geometry_msgs.msg import Twist         # geometry_msgs/Twist

# Other dependencies
import sys
import auxiliar

#threshold after remap
threshold_light = 50
light_l = 0
light_r = 0

# Standard Callbacks
def callback_light_l(vread):
    global light_l
    value = vread.intensity
    light_l = auxiliar.remap(value, data['sensorLeftBlackValue'], data['sensorLeftWhiteValue'], 0, 100)

def callback_light_r(vread):
    global light_r
    value = vread.intensity
    light_r = auxiliar.remap(value, data['sensorRightBlackValue'], data['sensorRightWhiteValue'], 0, 100)

# Callbacks for calibration
def callback_calib_l(data):
    global light_l
    light_l = data.intensity

def callback_calib_r(data):
    global light_r
    light_r = data.intensity

# calibration routine
def calibration():
    print "Iniciando calibracao"

    # obtem os valores para branco e preto de cada sensor
    raw_input("\nPosicione o robo com os sensores sobre o branco e digite enter...")
    data['sensorLeftWhiteValue'] = light_l
    data['sensorRightWhiteValue'] = light_r
    print "\nWhiteLeft = " + str(data['sensorLeftWhiteValue'])
    print "WhiteRight = " + str(data['sensorRightWhiteValue'])

    # TODO: deseja prosseguir ou fazer a medicao novamente??? 

    raw_input("\nPosicione o robo com os sensores sobre o preto e digite enter...")
    data['sensorRightBlackValue'] = light_r
    data['sensorLeftBlackValue'] = light_l
    print"\nBlackLeft = " + str(data['sensorLeftBlackValue'])
    print"BlackRight = " + str(data['sensorRightBlackValue'])
    
    # com remap 0-100 sendo executado eh possivel manter o threshold estavel em 50
    print "\n\nDados armazenados em JSON para remap dos sensores"
    # TODO: armazenar dados no arquivo json
    raw_input()

def line_follower():
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
        light_error = light_r - light_l
        #print "erro: " + str(light_error)

        # proportional control
        kp_linear = 0.00025
        kp_angular = 0.0035


        vel_msg.linear.x = 0.04 - abs(kp_linear * light_error)     # where kp * error can be up to 0.02 (max value for do not stop the car)
                                                                # 0.04 is an acceptable value for the velocity of the car
        vel_msg.angular.z = kp_angular * light_error            # kp * error, in this case, can be up to 0.25 with the experimental tests

        #print "linear: " + str(vel_msg.linear.x)
        #print "angular: " + str(vel_msg.angular.z)

        pub.publish(vel_msg)
        rate.sleep()

def main():
    # Load initial configs
    global data
    data = auxiliar.loadConfigs()

    rospy.init_node('light_control', anonymous=True)        # pra que??
    
    # Parser of calibration arg
    if len(sys.argv) > 1:
        # select the callbacks for the calibration
        sensor_l = rospy.Subscriber("/light_l", Light, callback_calib_l)
        sensor_r = rospy.Subscriber("/light_r", Light, callback_calib_r)

        globals()[sys.argv[1]]()

        sensor_l.unregister()
        sensor_r.unregister()

    # Line follower 
    rospy.Subscriber("/light_l", Light, callback_light_l)
    rospy.Subscriber("/light_r", Light, callback_light_r)

    line_follower()

if __name__ == '__main__':
    main()