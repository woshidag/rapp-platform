#include "ros/ros.h"
#include "rapp_platform_ros_communications/FindObjectsSrv.h"
#include "rapp_platform_ros_communications/LearnObjectSrv.h"
#include "rapp_platform_ros_communications/LoadModelsSrv.h"
#include "rapp_platform_ros_communications/ClearModelsSrv.h"

#include "rapp_object_recognition/find_objects.hpp"

std::map<std::string, FindObjects> detectors;

bool service_FindObjects(rapp_platform_ros_communications::FindObjectsSrv::Request  &req,
                         rapp_platform_ros_communications::FindObjectsSrv::Response &res)
{
  detectors[req.user].findObjects(req.user, req.fname, req.limit, res.found_names, res.found_centers, res.found_scores);
  return true;
}

bool service_LearnObject(rapp_platform_ros_communications::LearnObjectSrv::Request  &req,
                         rapp_platform_ros_communications::LearnObjectSrv::Response &res)
{
  detectors[req.user].learnObject(req.user, req.fname, req.name, res.result);
  return true;
}

bool service_LoadModels(rapp_platform_ros_communications::LoadModelsSrv::Request  &req,
                         rapp_platform_ros_communications::LoadModelsSrv::Response &res)
{
  detectors[req.user].loadModels(req.user, req.names, res.result);
  return true;
}

bool service_ClearModels(rapp_platform_ros_communications::ClearModelsSrv::Request  &req,
                         rapp_platform_ros_communications::ClearModelsSrv::Response &res)
{
  detectors[req.user].clearModels(req.user);
  return true;
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "find_objects_node");
  ros::NodeHandle n;

  std::string service_name;
  
  if (!n.getParam("/rapp_object_recognition_topic", service_name))
    ROS_ERROR("rapp_object_recogntion_topic not set!");
  ros::ServiceServer service = n.advertiseService(service_name, service_FindObjects);
  
  if (!n.getParam("/rapp_object_learn_topic", service_name))
    ROS_ERROR("rapp_object_learn_topic not set!");
  ros::ServiceServer service2 = n.advertiseService(service_name, service_LearnObject);
  
  if (!n.getParam("/rapp_object_load_topic", service_name))
    ROS_ERROR("rapp_object_load_topic not set!");
  ros::ServiceServer service3 = n.advertiseService(service_name, service_LoadModels);
  
  if (!n.getParam("/rapp_object_clear_topic", service_name))
    ROS_ERROR("rapp_object_clear_topic not set!");
  ros::ServiceServer service4 = n.advertiseService(service_name, service_ClearModels);
  
  ROS_INFO("Ready to find objects.");
  
  int threads = 1;
  if(!n.getParam("/rapp_object_recognition_threads", threads))
  {
    ROS_WARN("Hazard detection threads param not found");
  }
  else if(threads < 0)
  {
    threads = 1;
  }
  
  ROS_INFO("Ready to recognize!");
  ros::MultiThreadedSpinner spinner(threads);
  spinner.spin();
  
  
  //ros::spin();

  return 0;
}
