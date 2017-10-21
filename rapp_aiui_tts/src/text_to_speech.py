#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#Copyright 2015 RAPP

#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at

    #http://www.apache.org/licenses/LICENSE-2.0

#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

import rospy
import json
import sys
import os

from rapp_platform_ros_communications.srv import (
  TextToSpeechSrv,
  TextToSpeechSrvResponse
  )

from std_msgs.msg import String

from rapp_exceptions import RappError

class TextToSpeech:

  def __init__(self):
    # Speech recognition service published
    self.serv_topic = rospy.get_param("rapp_aiui_tts_topic")
    if(not self.serv_topic):
        rospy.logerror("Text to speech topic param not found")

    self.serv = rospy.Service(self.serv_topic, \
        TextToSpeechSrv, self.text_to_speech_callback)

    self.aiui_tts = rospy.Publisher('tts', String, queue_size=1)

  # The service callback
  def text_to_speech_callback(self, req):

    res = TextToSpeechSrvResponse()
    self.aiui_tts.publish(req.text)
    # req.text
    return res

if __name__ == "__main__":
  rospy.init_node('rapp_aiui_tts_ros_node')
  rapp_aiui_tts_ros_node = TextToSpeech()
  rospy.spin()


