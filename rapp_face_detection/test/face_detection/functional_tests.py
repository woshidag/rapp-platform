#!/usr/bin/env python
PKG='ros_nodes'

import sys
import unittest
import rospy
import roslib
import rospkg

from rapp_platform_ros_communications.srv import (
  FaceDetectionRosSrv,
  FaceDetectionRosSrvRequest
  )


class FaceDetFunc(unittest.TestCase):

    def test_faceExists(self):
        rospack = rospkg.RosPack()
        face_service = rospy.get_param("rapp_face_detection_detect_faces_topic")
        rospy.wait_for_service(face_service)
        fd_service = rospy.ServiceProxy(face_service, FaceDetectionRosSrv)
        req = FaceDetectionRosSrvRequest()
        req.imageFilename = rospack.get_path('rapp_auxiliary_files') + '/Lenna.png'
        response = fd_service(req)
        faces_num = len(response.faces_up_left)
        self.assertEqual( faces_num, 1 )
    
    def test_faceDoesNotExist(self):
        rospack = rospkg.RosPack()
        face_service = rospy.get_param("rapp_face_detection_detect_faces_topic")
        rospy.wait_for_service(face_service)
        fd_service = rospy.ServiceProxy(face_service, FaceDetectionRosSrv)
        req = FaceDetectionRosSrvRequest()
        req.imageFilename = rospack.get_path('rapp_auxiliary_files') + '/qr_code_rapp.jpg'
        response = fd_service(req)
        faces_num = len(response.faces_up_left)
        self.assertEqual( faces_num, 0 )
   
    def test_fileDoesNotExist(self):
        rospack = rospkg.RosPack()
        face_service = rospy.get_param("rapp_face_detection_detect_faces_topic")
        rospy.wait_for_service(face_service)
        fd_service = rospy.ServiceProxy(face_service, FaceDetectionRosSrv)
        req = FaceDetectionRosSrvRequest()
        req.imageFilename = rospack.get_path('rapp_auxiliary_files') + '/qr_code_rapp.png'
        response = fd_service(req)
        faces_num = len(response.faces_up_left)
        self.assertEqual( faces_num, 0 )
 
    def test_fileExistsButItAudio(self):
        rospack = rospkg.RosPack()
        face_service = rospy.get_param("rapp_face_detection_detect_faces_topic")
        rospy.wait_for_service(face_service)
        fd_service = rospy.ServiceProxy(face_service, FaceDetectionRosSrv)
        req = FaceDetectionRosSrvRequest()
        req.imageFilename = rospack.get_path('rapp_auxiliary_files') + '/silence_sample.wav'
        response = fd_service(req)
        faces_num = len(response.faces_up_left)
        self.assertEqual( faces_num, 0 )


if __name__ == '__main__':
    import rosunit
    rosunit.unitrun(PKG, 'FaceDetFunc', FaceDetFunc)














