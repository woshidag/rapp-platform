/***
 * Copyright 2015 RAPP
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * Authors: Konstantinos Panayiotou
 * Contact: klpanagi@gmail.com
 *
 */


/**
 * @fileOverview
 *
 * [Text-to-Speech] RAPP Platform front-end web service.
 *
 *  @author Konstantinos Panayiotou
 *  @copyright Rapp Project EU 2015
 */


var path = require('path');

var interfaces = require( path.join(__dirname, 'iface_obj.js') );

// const rosSrvName = "/add_pose";


/**
 *  [Text-To-Speech], RAPP Platform Front-End Web Service.
 *  Handles client requests for RAPP Platform Text-To-Speech Services.
 *
 *  Service Implementation
 *
 */
function svcImpl(req, resp, ros) {

  var rosMsg = new interfaces.ros_req();
  // console.log(req.body)
  // rosMsg.name = req.body.name;
  rosMsg = JSON.parse(req.body.data);
  rosSrvName = req.body.service;
  // ROS-Service response callback.
  function callback(data) {
    // Parse rosbridge message and craft client response
    var response = parseRosbridgeMsg(data);
    resp.sendJson(response);
  }

  // ROS-Service onerror callback.
  function onerror(e) {
    // Remove local file immediately.
    var response = new interfaces.client_res();
    response.error = e;
    resp.sendJson(response);
  }

  // Call ROS-Service.
  ros.callService(rosSrvName, rosMsg, {success: callback, fail: onerror});
}


/***
 *  Craft response object.
 *
 */
function parseRosbridgeMsg(rosbridge_msg) {
  const error = rosbridge_msg.error;
  var response = new interfaces.client_res();

  response = rosbridge_msg;

  if (error) {
    response.error = error;
    return response;
  }

  return response;
}


module.exports = svcImpl;
