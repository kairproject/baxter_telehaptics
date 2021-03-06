#!/usr/bin/env python
#----------------------------------------------------------------------
# Tasks:
# 1. Listens to topic 'move_done'
# 2. Continually publishes poses to make Baxter's arm draw a "triangle"
#
# Last updated 4/1/17
#----------------------------------------------------------------------

import rospy
from std_msgs.msg import Bool
from geometry_msgs.msg import Pose, Point, Quaternion

#Global
NEW_MOVE = False

def give_move_cb(give_move_flag): #Get status of commander
    #True if commander ready for next move
    global NEW_MOVE
    NEW_MOVE = give_move_flag

def draw_circle(index):
    #Creating publisher for trajectory
    ui_pub = rospy.Publisher('ui_output', Pose, queue_size = 3)
    #Creating publisher for telling command to start velocity control
    sent_move_pub = rospy.Publisher('sent_move', Bool, queue_size = 3)

    coord = Pose()

    if NEW_MOVE == True:
        if index == 0:
            rospy.logerr("Point 1")
            coord = Pose(
              position = Point(
                x = 0.699492549605,
                y = -0.512625185718,
                z = 0.155200699953,
              ),
              orientation = Quaternion(
                x = 0.964986309494,
                y = 0.241992573035,
                z = 0.0686445919972,
                w = 0.0743568226546,
            ))

        # elif index == 1:
        #     rospy.logerr("Point 2")
        #     coord = Pose(
        #       position = Point(
        #         x = 0.526334454121,
        #         y =  -0.679712790491,
        #         z =  0.17463829815,
        #       ),
        #       orientation = Quaternion(
        #         x =  0.968038006195,
        #         y = 0.250115601298,
        #         z =-0.00435745787217,
        #         w = 0.0180448638477,
        #     ))

        ui_pub.publish(coord)            # Sending move
        sent_move_flag.publish(True)     # Tell cmd move was sent
        index = index + 1

if __name__ == '__main__':
    rospy.init_node('drawshape_ui')

    #Creating subscriber for listening to arm status
    rospy.Subscriber('give_move', Bool, give_move_cb)

    point_index = 0
    while not rospy.is_shutdown():
        draw_circle(point_index)

    rospy.spin()
