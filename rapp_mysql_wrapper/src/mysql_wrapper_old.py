#!/usr/bin/env python

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

# Author: Athanassios Kintsakis
# contact: akintsakis@issel.ee.auth.gr

import rospy
import MySQLdb as mdb
import sys

from rapp_platform_ros_communications.srv import (
  fetchDataSrv,
  fetchDataSrvResponse,
  writeDataSrv,
  writeDataSrvResponse,
  deleteDataSrv,
  deleteDataSrvResponse,
  updateDataSrv,
  updateDataSrvResponse,
  whatRappsCanRunSrv,
  whatRappsCanRunSrvResponse,
  authTokenByServiceSrv,
  authTokenByServiceSrvResponse,
  )

from rapp_platform_ros_communications.msg import (
  StringArrayMsg
  )

from std_msgs.msg import (
  String
  )
  
## @class MySQLdbWrapper
# @brief The mysql wrapper ros node
class MySQLdbWrapper:

  ## @brief Default contructor
  #
  # Declares the callbacks of the node's services
  def __init__(self):
    #tblUser services launch
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_user_fetch_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_user_fetch_data_topic")
    self.serv=rospy.Service(self.serv_topic, fetchDataSrv, self.tblUserFetchDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_user_write_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_user_write_data_topic")
    self.serv=rospy.Service(self.serv_topic, writeDataSrv, self.tblUserWriteDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_user_delete_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_user_delete_data_topic")
    self.serv=rospy.Service(self.serv_topic, deleteDataSrv, self.tblUserDeleteDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_user_update_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_user_update_data_topic")
    self.serv=rospy.Service(self.serv_topic, updateDataSrv, self.tblUserUpdateDataHandler)
    #tblModel services launch
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_model_fetch_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_model_fetch_data_topic")
    self.serv=rospy.Service(self.serv_topic, fetchDataSrv, self.tblModelFetchDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_model_write_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_model_write_data_topic")
    self.serv=rospy.Service(self.serv_topic, writeDataSrv, self.tblModelWriteDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_model_delete_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_model_delete_data_topic")
    self.serv=rospy.Service(self.serv_topic, deleteDataSrv, self.tblModelDeleteDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_model_update_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_model_update_data_topic")
    self.serv=rospy.Service(self.serv_topic, updateDataSrv, self.tblModelUpdateDataHandler)
    #tblRapp services launch
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_rapp_fetch_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_rapp_fetch_data_topic")
    self.serv=rospy.Service(self.serv_topic, fetchDataSrv, self.tblRappFetchDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_rapp_write_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_rapp_write_data_topic")
    self.serv=rospy.Service(self.serv_topic, writeDataSrv, self.tblRappWriteDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_rapp_delete_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_rapp_delete_data_topic")
    self.serv=rospy.Service(self.serv_topic, deleteDataSrv, self.tblRappDeleteDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_rapp_update_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_rapp_update_data_topic")
    self.serv=rospy.Service(self.serv_topic, updateDataSrv, self.tblRappUpdateDataHandler)
    #tblRobot services launch
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_robot_fetch_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_robot_fetch_data_topic")
    self.serv=rospy.Service(self.serv_topic, fetchDataSrv, self.tblRobotFetchDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_robot_write_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_robot_write_data_topic")
    self.serv=rospy.Service(self.serv_topic, writeDataSrv, self.tblRobotWriteDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_robot_delete_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_robot_delete_data_topic")
    self.serv=rospy.Service(self.serv_topic, deleteDataSrv, self.tblRobotDeleteDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_robot_update_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_robot_update_data_topic")
    self.serv=rospy.Service(self.serv_topic, updateDataSrv, self.tblRobotUpdateDataHandler)
    #tblAppsRobots services launch
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_apps_robots_fetch_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_apps_robots_fetch_data_topic")
    self.serv=rospy.Service(self.serv_topic, fetchDataSrv, self.tblAppsRobotsFetchDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_apps_robots_write_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_apps_robots_write_data_topic")
    self.serv=rospy.Service(self.serv_topic, writeDataSrv, self.tblAppsRobotsWriteDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_apps_robots_delete_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_apps_robots_delete_data_topic")
    self.serv=rospy.Service(self.serv_topic, deleteDataSrv, self.tblAppsRobotsDeleteDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_apps_robots_update_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_apps_robots_update_data_topic")
    self.serv=rospy.Service(self.serv_topic, updateDataSrv, self.tblAppsRobotsUpdateDataHandler)
    #tblUsersOntologyInstances services launch
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_users_ontology_instances_fetch_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_users_ontology_instances_fetch_data_topic")
    self.serv=rospy.Service(self.serv_topic, fetchDataSrv, self.tblUsersOntologyInstancesFetchDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_users_ontology_instances_write_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_users_ontology_instances_write_data_topic")
    self.serv=rospy.Service(self.serv_topic, writeDataSrv, self.tblUsersOntologyInstancesWriteDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_users_ontology_instances_delete_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_users_ontology_instances_delete_data_topic")
    self.serv=rospy.Service(self.serv_topic, deleteDataSrv, self.tblUsersOntologyInstancesDeleteDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_users_ontology_instances_update_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_users_ontology_instances_update_data_topic")
    self.serv=rospy.Service(self.serv_topic, updateDataSrv, self.tblUsersOntologyInstancesUpdateDataHandler)
    #viewUsersRobotsApps services launch
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_view_users_robots_apps_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_view_users_robots_apps_topic")
    self.serv=rospy.Service(self.serv_topic, fetchDataSrv, self.viewUsersRobotsAppsFetchDataHandler)

    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_what_rapps_can_run_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_what_rapps_can_run Not found error")
    self.serv=rospy.Service(self.serv_topic, whatRappsCanRunSrv, self.whatRappsCanRunDataHandler)
    
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_auth_token_by_service_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_auth_token_by_service_topic Not found error")
    self.serv=rospy.Service(self.serv_topic, authTokenByServiceSrv, self.authTokenByServiceDataHandler)    
        
    
    #cloud agent tables
    #cloud_agent services launch
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_cloud_agent_fetch_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_cloud_agent_fetch_data_topic")
    self.serv=rospy.Service(self.serv_topic, fetchDataSrv, self.tblCloudAgentFetchDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_cloud_agent_write_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_cloud_agent_write_data_topic")
    self.serv=rospy.Service(self.serv_topic, writeDataSrv, self.tblCloudAgentWriteDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_cloud_agent_delete_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_cloud_agent_delete_data_topic")
    self.serv=rospy.Service(self.serv_topic, deleteDataSrv, self.tblCloudAgentDeleteDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_cloud_agent_update_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_cloud_agent_update_data_topic")
    self.serv=rospy.Service(self.serv_topic, updateDataSrv, self.tblCloudAgentUpdateDataHandler)
    
    #cloud_agent_service services launch
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_cloud_agent_service_fetch_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_cloud_agent_service_fetch_data_topic")
    self.serv=rospy.Service(self.serv_topic, fetchDataSrv, self.tblCloudAgentServiceFetchDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_cloud_agent_service_write_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_cloud_agent_service_write_data_topic")
    self.serv=rospy.Service(self.serv_topic, writeDataSrv, self.tblCloudAgentServiceWriteDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_cloud_agent_service_delete_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_cloud_agent_service_delete_data_topic")
    self.serv=rospy.Service(self.serv_topic, deleteDataSrv, self.tblCloudAgentServiceDeleteDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_cloud_agent_service_update_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_cloud_agent_service_update_data_topic")
    self.serv=rospy.Service(self.serv_topic, updateDataSrv, self.tblCloudAgentServiceUpdateDataHandler)

    #cloud_agent_service_arguments_ services launch
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_cloud_agent_service_arguments_fetch_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_cloud_agent_service_arguments_fetch_data_topic")
    self.serv=rospy.Service(self.serv_topic, fetchDataSrv, self.tblCloudAgentServiceArgumentsFetchDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_cloud_agent_service_arguments_write_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_cloud_agent_service_arguments_write_data_topic")
    self.serv=rospy.Service(self.serv_topic, writeDataSrv, self.tblCloudAgentServiceArgumentsWriteDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_cloud_agent_service_arguments_delete_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_cloud_agent_service_arguments_delete_data_topic")
    self.serv=rospy.Service(self.serv_topic, deleteDataSrv, self.tblCloudAgentServiceArgumentsDeleteDataHandler)
    self.serv_topic = rospy.get_param("rapp_mysql_wrapper_cloud_agent_service_arguments_update_data_topic")
    if(not self.serv_topic):
      rospy.logerror("rapp_mysql_wrapper_cloud_agent_service_arguments_update_data_topic")
    self.serv=rospy.Service(self.serv_topic, updateDataSrv, self.tblCloudAgentServiceArgumentsUpdateDataHandler)

  ## @brief Implements the general write data to table function
  # @param req [rapp_platform_ros_communications::writeDataSrvRequest::Request&] The ROS service request
  # @param tblName [string] the table name
  # @param res [rapp_platform_ros_communications::writeDataResponse::Response&] The ROS service response
  def writeData(self,req,tblName):
    try:
      print tblName
      res = writeDataSrvResponse()
      db_username,db_password=self.getLogin()
      con = mdb.connect('localhost', db_username, db_password, 'RappStore');
      cur = con.cursor()
      returncols=self.constructCommaColumns(req.req_cols)
      if (len(returncols)>1):
        returncols="("+returncols+")"
      print returncols
      values=""
      for i in range(len(req.req_data)):
        if (i==0):
          values=values+"("+self.constructCommaColumns(req.req_data[i].s)+")"
        else:
          values=values+",("+self.constructCommaColumns(req.req_data[i].s)+")"

      query="Insert into "+tblName+" "+ returncols+" values "+values
      cur.execute("LOCK TABLES "+tblName+" WRITE")
      cur.execute(query)
      cur.execute("UNLOCK TABLES")
      con.close()
      res.success.data=True
      res.trace.append("Success")
    except mdb.Error, e:
      res.trace.append(("Database Error %d: %s" % (e.args[0],e.args[1])))
      res.success.data=False
      res.error="Error %d: %s" % (e.args[0],e.args[1])
    except IndexError, e:
      res.trace.append("IndexError: " +str(e))
      res.success.data=False
      res.error="IndexError: " +str(e)
    except IOError, e:      
      res.success.data=False
      res.trace.append("IOError: " +str(e))
      res.error="IOError: " +str(e)
    return res

  ## @brief Implements the general delete data from table function
  # @param req [rapp_platform_ros_communications::deleteDataSrvRequest::Request&] The ROS service request
  # @param tblName [string] the table name
  # @param res [rapp_platform_ros_communications::deleteDataSrvResponse::Response&] The ROS service response
  def deleteData(self,req,tblName):
    try:
      res = deleteDataSrvResponse()
      db_username,db_password=self.getLogin()
      con = mdb.connect('localhost', db_username, db_password, 'RappStore');
      cur = con.cursor()
      where=self.constructAndQuery(req.where_data)
      query="Delete from "+tblName+where
      cur.execute("LOCK TABLES "+tblName+" WRITE")
      cur.execute(query)
      cur.execute("UNLOCK TABLES")
      con.close()
      res.success.data=True
      res.trace.append("Success")
    except mdb.Error, e:
      res.trace.append(("Database Error %d: %s" % (e.args[0],e.args[1])))
      res.success.data=False
      res.error="Error %d: %s" % (e.args[0],e.args[1])
    except IndexError, e:
      res.trace.append("IndexError: " +str(e))
      res.success.data=False
      res.error="IndexError: " +str(e)
    except IOError, e:      
      res.success.data=False
      res.trace.append("IOError: " +str(e))
      res.error="IOError: " +str(e)
    return res

  ## @brief Implements the general update data from table function
  # @param req [rapp_platform_ros_communications::updateDataSrvRequest::Request&] The ROS service request
  # @param tblName [string] the table name
  # @param res [rapp_platform_ros_communications::updateDataSrvResponse::Response&] The ROS service response
  def updateData(self,req,tblName):
    try:
      res = updateDataSrvResponse()
      db_username,db_password=self.getLogin()
      con = mdb.connect('localhost', db_username, db_password, 'RappStore');
      cur = con.cursor()
      returncols=self.constructCommaColumns(req.set_cols)
      where=self.constructAndQuery(req.where_data)
      query="Update "+tblName+" SET "+returncols+where
      print query
      cur.execute("LOCK TABLES "+tblName+" WRITE")
      cur.execute(query)
      cur.execute("UNLOCK TABLES")
      con.close()
      res.success.data=True
      res.trace.append("Success")
    except mdb.Error, e:
      res.trace.append(("Database Error %d: %s" % (e.args[0],e.args[1])))
      res.success.data=False
      res.error="Error %d: %s" % (e.args[0],e.args[1])
    except IndexError, e:
      res.trace.append("IndexError: " +str(e))
      res.success.data=False
      res.error="IndexError: " +str(e)
    except IOError, e:      
      res.success.data=False
      res.trace.append("IOError: " +str(e))
      res.error="IOError: " +str(e)
    return res

  ## @brief Implements the general fetch data from table function
  # @param req [rapp_platform_ros_communications::fetchDataSrvRequest::Request&] The ROS service request
  # @param tblName [string] the table name
  # @param res [rapp_platform_ros_communications::fetchDataSrvResponse::Response&] The ROS service response
  def fetchData(self,req,tblName):
    try:
      res = fetchDataSrvResponse()
      db_username,db_password=self.getLogin()
      con = mdb.connect('localhost', db_username, db_password, 'RappStore');
      cur = con.cursor()
      returncols=self.constructCommaColumns(req.req_cols)
      where=self.constructAndQuery(req.where_data)
      query="SELECT "+returncols+" FROM "+tblName+where
      cur.execute(query)
      result_set = cur.fetchall()
      for i in range(len(result_set)):
        line=StringArrayMsg()
        for j in range(len(result_set[i])):
          temp_s=String(result_set[i][j])
          line.s.append((str(result_set[i][j])))
        res.res_data.append(line)

      con.close()
      if (returncols=="*"):
        res.res_cols=self.getTableColumnNames(tblName)
      else:
        res.res_cols=req.req_cols
      con.close()
      res.success.data=True
      res.trace.append("Success")
    except mdb.Error, e:
      res.trace.append(("Database Error %d: %s" % (e.args[0],e.args[1])))
      res.success.data=False
      res.error="Error %d: %s" % (e.args[0],e.args[1])
    except IndexError, e:
      res.trace.append("IndexError: " +str(e))
      res.success.data=False
      res.error="IndexError: " +str(e)
    except IOError, e:      
      res.success.data=False
      res.trace.append("IOError: " +str(e))
      res.error="IOError: " +str(e)
    return res

  ## @brief Implements the whatRappsCanRun service
  # @param req [rapp_platform_ros_communications::whatRappsCanRunSrvResponse::Request&] The ROS service request
  # @param tblName [string] the table name
  # @param res [rapp_platform_ros_communications::whatRappsCanRunSrvResponse::Response&] The ROS service response
  def whatRappsCanRun(self,req,tblName):
    try:
      res = whatRappsCanRunSrvResponse()
      db_username,db_password=self.getLogin()
      con = mdb.connect('localhost', db_username, db_password, 'RappStore');
      cur = con.cursor()
      query="SELECT rapp_id from tblRappsModelsVersion where model_id='"+req.model_id+"' and minimum_coreagent_version<='"+req.core_agent_version+"'";
      cur.execute(query)
      result_set = cur.fetchall()
      for i in range(len(result_set)):
        line=StringArrayMsg()
        for j in range(len(result_set[i])):
          temp_s=String(result_set[i][j])
          line.s.append((str(result_set[i][j])))
        res.res_data.append(line)
      con.close()
      res.success.data=True
      res.trace.append("Success")
    except mdb.Error, e:
      res.trace.append(("Database Error %d: %s" % (e.args[0],e.args[1])))
      res.success.data=False
      res.error="Error %d: %s" % (e.args[0],e.args[1])
    except IndexError, e:
      res.trace.append("IndexError: " +str(e))
      res.success.data=False
      res.error="IndexError: " +str(e)
    except IOError, e:      
      res.success.data=False
      res.trace.append("IOError: " +str(e))
      res.error="IOError: " +str(e)
    return res

  def authTokenByService(self,req):
    try:
      res = authTokenByServiceSrvResponse()  
      res.authentication_success=False  
      db_username,db_password=self.getLogin()
      con = mdb.connect('localhost', db_username, db_password, 'RappStore');
      cur = con.cursor()
      cur.execute("select service_name from application_token_services where token_id=(select id from application_token where token=%s) and service_name=%s",(req.token,req.service_name))   
      result_set = cur.fetchall()
      print result_set
      if(result_set and len(result_set[0])>0):
        if(result_set[0][0]==req.service_name):
          res.authentication_success=True
      else:
        cur.execute("select service_name from application_token_services where token_id=(select id from application_token where token=%s) and service_name='*'",(req.token))   
        result_set = cur.fetchall()
        if(result_set and len(result_set[0])>0 ):
          if(result_set[0][0]=='*'):
            res.authentication_success=True
      con.close()
      res.success=True
    except mdb.Error, e:
      res.trace.append(("Database Error %d: %s" % (e.args[0],e.args[1])))
      res.success=False
      res.error="Error %d: %s" % (e.args[0],e.args[1])
    #except IndexError, e:
      #res.trace.append("IndexError: " +str(e))
      #res.success=False
      #res.error="IndexError: " +str(e)
    except IOError, e:      
      res.success=False
      res.trace.append("IOError: " +str(e))
      res.error="IOError: " +str(e)
    return res  
    
  ## @brief Places commas between columns and constructs a string
  # @param cols [list] the input columns
  # @return returncols [string] the output string
  def constructCommaColumns(self,cols):
    #assisting function. adds commas between columns
    if (len(cols)<1):
      return ""
    elif (cols[0]=="*"):
      return "*"
    else:
      returncols=""
      for i in range(len(cols)):
          if i==0:
            returncols=returncols+cols[i]
          else:
            returncols=returncols+","+cols[i]
      return returncols

  ## @brief Construcs the where= ..and where=... clause
  # @param cols [list] the columns needed to construct the clause
  # @return returnquery [string] the And clause
  def constructAndQuery(self,cols):
    returnquery=""
    if(len(cols)==0):
      return ""
    else:
      for i in range(len(cols)):
        if i==0:
          returnquery=returnquery+cols[i].s[0]+"=\""+cols[i].s[1]+"\""
        else:
          returnquery=returnquery+" AND "+cols[i].s[0]+"=\""+cols[i].s[1]+"\""
      returnquery=" WHERE "+returnquery
      return returnquery

  ## @brief Gets the columns of the table
  # @return Columns [list] the columns of the table
  def getTableColumnNames(self,tblName):
    db_username,db_password=self.getLogin()
    try:
      con = mdb.connect('localhost', db_username, db_password, 'RappStore');
      cur = con.cursor()
      cur.execute("Show columns from "+tblName)
      result_set = cur.fetchall()
      Columns=[]
      for row in result_set:
        Columns=Columns+[String(str(row[0]))]
      return Columns
    except mdb.Error, e:
      print "Error %d: %s" % (e.args[0],e.args[1])

  ## @brief Loads login details from file
  # @return [ void ] Login details loaded successfully
  def getLogin(self): 
    fh = open("/etc/db_credentials", "r")
    db_username=fh.readline()
    db_username=db_username.split( )[0]
    db_password=fh.readline()
    db_password=db_password.split()[0]
    return db_username,db_password

  ## @brief Checks connectivity to the DB
  # @return [ void ] Connection performed successfully
  def checkConnection(self):
    try:
      db_username,db_password=self.getLogin()
      con = mdb.connect('localhost', db_username, db_password, 'RappStore')
      cur = con.cursor()
      cur.execute("SELECT VERSION()")
      ver = cur.fetchone()
      print "Database version : %s " % ver
      con.close()
    except mdb.Error, e:
      print "Error %d: %s" % (e.args[0],e.args[1])

  ## @brief The tbl user fetch data service callback
  # @param req [rapp_platform_ros_communications::fetchDataSrvRequest::Request&] The ROS service request
  # @param res [rapp_platform_ros_communications::fetchDataSrvResponse::Response&] The ROS service response
  def tblUserFetchDataHandler(self,req):
    res = fetchDataSrvResponse()
    res=self.fetchData(req,"users")
    return res

  ## @brief The tbl user write data service callback
  # @param req [rapp_platform_ros_communications::writeDataSrvRequest::Request&] The ROS service request
  # @param res [rapp_platform_ros_communications::writeDataResponse::Response&] The ROS service response
  def tblUserWriteDataHandler(self,req):
    res = writeDataSrvResponse()
    res=self.writeData(req,"users")
    return res

  ## @brief The tbl user delete data service callback
  # @param req [rapp_platform_ros_communications::deleteDataSrvRequest::Request&] The ROS service request
  # @param res [rapp_platform_ros_communications::deleteDataSrvResponse::Response&] The ROS service response
  def tblUserDeleteDataHandler(self,req):
    res = deleteDataSrvResponse()
    res=self.deleteData(req,"users")
    return res

  ## @brief The tbl user update data service callback
  # @param req [rapp_platform_ros_communications::updateDataSrvRequest::Request&] The ROS service request
  # @param res [rapp_platform_ros_communications::updateDataSrvResponse::Response&] The ROS service response
  def tblUserUpdateDataHandler(self,req):
    res = updateDataSrvResponse()
    res=self.updateData(req,"users")
    return res

  ## @brief The tbl model fetch data service callback
  # @param req [rapp_platform_ros_communications::fetchDataSrvRequest::Request&] The ROS service request
  # @param res [rapp_platform_ros_communications::fetchDataSrvResponse::Response&] The ROS service response
  def tblModelFetchDataHandler(self,req):
    res = fetchDataSrvResponse()
    res=self.fetchData(req,"tblModel")
    return res

  ## @brief The tbl model write data service callback
  # @param req [rapp_platform_ros_communications::writeDataSrvRequest::Request&] The ROS service request
  # @param res [rapp_platform_ros_communications::writeDataSrvResponse::Response&] The ROS service response
  def tblModelWriteDataHandler(self,req):
    res = writeDataSrvResponse()
    res=self.writeData(req,"tblModel")
    return res

  ## @brief The tbl model delete data service callback
  # @param req [rapp_platform_ros_communications::deleteDataSrvRequest::Request&] The ROS service request
  # @param res [rapp_platform_ros_communications::deleteDataSrvResponse::Response&] The ROS service response
  def tblModelDeleteDataHandler(self,req):
    res = deleteDataSrvResponse()
    res=self.deleteData(req,"tblModel")
    return res

  ## @brief The tbl model update data service callback
  # @param req [rapp_platform_ros_communications::updateDataSrvRequest::Request&] The ROS service request
  # @param res [rapp_platform_ros_communications::updateDataSrvResponse::Response&] The ROS service response
  def tblModelUpdateDataHandler(self,req):
    res = updateDataSrvResponse()
    res=self.updateData(req,"tblModel")
    return res

  ## @brief The tbl rapp fetch data service callback
  # @param req [rapp_platform_ros_communications::fetchDataSrvRequest::Request&] The ROS service request
  # @param res [rapp_platform_ros_communications::fetchDataSrvResponse::Response&] The ROS service response
  def tblRappFetchDataHandler(self,req):
    res = fetchDataSrvResponse()
    res=self.fetchData(req,"tblRapp")
    return res

  ## @brief The tbl rapp write data service callback
  # @param req [rapp_platform_ros_communications::writeDataSrvRequest::Request&] The ROS service request
  # @param res [rapp_platform_ros_communications::writeDataResponse::Response&] The ROS service response
  def tblRappWriteDataHandler(self,req):
    res = writeDataSrvResponse()
    res=self.writeData(req,"tblRapp")
    return res

  ## @brief The tbl rapp delete data service callback
  # @param req [rapp_platform_ros_communications::deleteDataSrvRequest::Request&] The ROS service request
  # @param res [rapp_platform_ros_communications::deleteDataSrvResponse::Response&] The ROS service response
  def tblRappDeleteDataHandler(self,req):
    res = deleteDataSrvResponse()
    res=self.deleteData(req,"tblRapp")
    return res

  ## @brief The tbl rapp update data service callback
  # @param req [rapp_platform_ros_communications::updateDataSrvRequest::Request&] The ROS service request
  # @param res [rapp_platform_ros_communications::updateDataSrvResponse::Response&] The ROS service response
  def tblRappUpdateDataHandler(self,req):
    res = updateDataSrvResponse()
    res=self.updateData(req,"robots")
    return res

  ## @brief The tbl robot fetch data service callback
  # @param req [rapp_platform_ros_communications::fetchDataSrvRequest::Request&] The ROS service request
  # @param res [rapp_platform_ros_communications::fetchDataSrvResponse::Response&] The ROS service response
  def tblRobotFetchDataHandler(self,req):
    res = fetchDataSrvResponse()
    res=self.fetchData(req,"robots")
    return res

  ## @brief The tbl robot write data service callback
  # @param req [rapp_platform_ros_communications::writeDataSrvRequest::Request&] The ROS service request
  # @param res [rapp_platform_ros_communications::writeDataResponse::Response&] The ROS service response
  def tblRobotWriteDataHandler(self,req):
    res = writeDataSrvResponse()
    res=self.writeData(req,"robots")
    return res

  ## @brief The tbl robot delete data service callback
  # @param req [rapp_platform_ros_communications::deleteDataSrvRequest::Request&] The ROS service request
  # @param res [rapp_platform_ros_communications::deleteDataSrvResponse::Response&] The ROS service response
  def tblRobotDeleteDataHandler(self,req):
    res = deleteDataSrvResponse()
    res=self.deleteData(req,"robots")
    return res

  ## @brief The tbl robot update data service callback
  # @param req [rapp_platform_ros_communications::updateDataSrvRequest::Request&] The ROS service request
  # @param res [rapp_platform_ros_communications::updateDataSrvResponse::Response&] The ROS service response
  def tblRobotUpdateDataHandler(self,req):
    res = updateDataSrvResponse()
    res=self.updateData(req,"robots")
    return res

  ## @brief The tbl appsRobots fetch data service callback
  # @param req [rapp_platform_ros_communications::fetchDataSrvRequest::Request&] The ROS service request
  # @param res [rapp_platform_ros_communications::fetchDataSrvResponse::Response&] The ROS service response
  def tblAppsRobotsFetchDataHandler(self,req):
    res = fetchDataSrvResponse()
    res=self.fetchData(req,"tblAppsRobots")
    return res

  ## @brief The tbl appsRobots write data service callback
  # @param req [rapp_platform_ros_communications::writeDataSrvRequest::Request&] The ROS service request
  # @param res [rapp_platform_ros_communications::writeDataResponse::Response&] The ROS service response
  def tblAppsRobotsWriteDataHandler(self,req):
    res = writeDataSrvResponse()
    res=self.writeData(req,"tblAppsRobots")
    return res

  ## @brief The tbl appsRobots delete data service callback
  # @param req [rapp_platform_ros_communications::deleteDataSrvRequest::Request&] The ROS service request
  # @param res [rapp_platform_ros_communications::deleteDataSrvResponse::Response&] The ROS service response
  def tblAppsRobotsDeleteDataHandler(self,req):
    res = deleteDataSrvResponse()
    res=self.deleteData(req,"tblAppsRobots")
    return res

  ## @brief The tbl appsRobots update data service callback
  # @param req [rapp_platform_ros_communications::updateDataSrvRequest::Request&] The ROS service request
  # @param res [rapp_platform_ros_communications::updateDataSrvResponse::Response&] The ROS service response
  def tblAppsRobotsUpdateDataHandler(self,req):
    res = updateDataSrvResponse()
    res=self.updateData(req,"tblAppsRobots")
    return res

  ## @brief The tbl usersOntologyInstances fetch data service callback
  # @param req [rapp_platform_ros_communications::fetchDataSrvRequest::Request&] The ROS service request
  # @param res [rapp_platform_ros_communications::fetchDataSrvResponse::Response&] The ROS service response
  def tblUsersOntologyInstancesFetchDataHandler(self,req):
    res = fetchDataSrvResponse()
    res=self.fetchData(req,"tblUsersOntologyInstances")
    return res

  ## @brief The tbl usersOntologyInstances write data service callback
  # @param req [rapp_platform_ros_communications::writeDataSrvRequest::Request&] The ROS service request
  # @param res [rapp_platform_ros_communications::writeDataResponse::Response&] The ROS service response
  def tblUsersOntologyInstancesWriteDataHandler(self,req):
    res = writeDataSrvResponse()
    res=self.writeData(req,"tblUsersOntologyInstances")
    return res

  ## @brief The tbl usersOntologyInstances delete data service callback
  # @param req [rapp_platform_ros_communications::deleteDataSrvRequest::Request&] The ROS service request
  # @param res [rapp_platform_ros_communications::deleteDataSrvResponse::Response&] The ROS service response
  def tblUsersOntologyInstancesDeleteDataHandler(self,req):
    res = deleteSrvResponse()
    res=self.deleteData(req,"tblUsersOntologyInstances")
    return res
    
  ## @brief The tbl usersOntologyInstances update data service callback
  # @param req [rapp_platform_ros_communications::updateDataSrvRequest::Request&] The ROS service request
  # @param res [rapp_platform_ros_communications::updateDataSrvResponse::Response&] The ROS service response
  def tblUsersOntologyInstancesUpdateDataHandler(self,req):
    res = updateDataSrvResponse()
    res=self.updateData(req,"tblUsersOntologyInstances")
    return res

  ## @brief The view usersRobotsApps fetch data service callback
  # @param req [rapp_platform_ros_communications::fetchDataSrvRequest::Request&] The ROS service request
  # @param res [rapp_platform_ros_communications::fetchDataSrvResponse::Response&] The ROS service response
  def viewUsersRobotsAppsFetchDataHandler(self,req):
    res = fetchDataSrvResponse()
    res=self.fetchData(req,"usersrobotsapps")
    return res

  ## @brief The what rappRappCanRun service callback
  # @param req [rapp_platform_ros_communications::whatRappsCanRunSrvResponse::Request&] The ROS service request
  # @param res [rapp_platform_ros_communications::whatRappsCanRunSrvRequest::Response&] The ROS service response
  def whatRappsCanRunDataHandler(self,req):
    res = whatRappsCanRunSrvResponse()
    res=self.whatRappsCanRun(req,"tblRappsModelsVersion")
    return res

  ## @brief The authTokenByService service callback
  # @param req [rapp_platform_ros_communications::authTokenByServiceSrvResponse::Request&] The ROS service request
  # @param res [rapp_platform_ros_communications::authTokenByServiceSrvRequest::Response&] The ROS service response
  def authTokenByServiceDataHandler(self,req):
    res = authTokenByServiceSrvResponse()
    res=self.authTokenByService(req)
    return res

#cloud agent callbacks

  ## @brief The tbl cloud_agent fetch data service callback
  # @param req [rapp_platform_ros_communications::fetchDataSrvRequest::Request&] The ROS service request
  # @param res [rapp_platform_ros_communications::fetchDataSrvResponse::Response&] The ROS service response
  def tblCloudAgentFetchDataHandler(self,req):
    res = fetchDataSrvResponse()
    res=self.fetchData(req,"cloud_agent")
    return res

  ## @brief The tbl cloud_agent write data service callback
  # @param req [rapp_platform_ros_communications::writeDataSrvRequest::Request&] The ROS service request
  # @param res [rapp_platform_ros_communications::writeDataResponse::Response&] The ROS service response
  def tblCloudAgentWriteDataHandler(self,req):
    res = writeDataSrvResponse()
    res=self.writeData(req,"cloud_agent")
    return res

  ## @brief The tbl cloud_agent delete data service callback
  # @param req [rapp_platform_ros_communications::deleteDataSrvRequest::Request&] The ROS service request
  # @param res [rapp_platform_ros_communications::deleteDataSrvResponse::Response&] The ROS service response
  def tblCloudAgentDeleteDataHandler(self,req):
    res = deleteDataSrvResponse()
    res=self.deleteData(req,"cloud_agent")
    return res

  ## @brief The tbl cloud_agent update data service callback
  # @param req [rapp_platform_ros_communications::updateDataSrvRequest::Request&] The ROS service request
  # @param res [rapp_platform_ros_communications::updateDataSrvResponse::Response&] The ROS service response
  def tblCloudAgentUpdateDataHandler(self,req):
    res = updateDataSrvResponse()
    res=self.updateData(req,"cloud_agent")
    return res

  ## @brief The tbl cloud_agent_service fetch data service callback
  # @param req [rapp_platform_ros_communications::fetchDataSrvRequest::Request&] The ROS service request
  # @param res [rapp_platform_ros_communications::fetchDataSrvResponse::Response&] The ROS service response
  def tblCloudAgentServiceFetchDataHandler(self,req):
    res = fetchDataSrvResponse()
    res=self.fetchData(req,"cloud_agent_service")
    return res

  ## @brief The tbl cloud_agent_service write data service callback
  # @param req [rapp_platform_ros_communications::writeDataSrvRequest::Request&] The ROS service request
  # @param res [rapp_platform_ros_communications::writeDataResponse::Response&] The ROS service response
  def tblCloudAgentServiceWriteDataHandler(self,req):
    res = writeDataSrvResponse()
    res=self.writeData(req,"cloud_agent_service")
    return res

  ## @brief The tbl cloud_agent_service delete data service callback
  # @param req [rapp_platform_ros_communications::deleteDataSrvRequest::Request&] The ROS service request
  # @param res [rapp_platform_ros_communications::deleteDataSrvResponse::Response&] The ROS service response
  def tblCloudAgentServiceDeleteDataHandler(self,req):
    res = deleteDataSrvResponse()
    res=self.deleteData(req,"cloud_agent_service")
    return res

  ## @brief The tbl cloud_agent_service update data service callback
  # @param req [rapp_platform_ros_communications::updateDataSrvRequest::Request&] The ROS service request
  # @param res [rapp_platform_ros_communications::updateDataSrvResponse::Response&] The ROS service response
  def tblCloudAgentServiceUpdateDataHandler(self,req):
    res = updateDataSrvResponse()
    res=self.updateData(req,"cloud_agent_service")
    return res
    
  ## @brief The tbl cloud_agent_service_arguments fetch data service callback
  # @param req [rapp_platform_ros_communications::fetchDataSrvRequest::Request&] The ROS service request
  # @param res [rapp_platform_ros_communications::fetchDataSrvResponse::Response&] The ROS service response
  def tblCloudAgentServiceArgumentsFetchDataHandler(self,req):
    res = fetchDataSrvResponse()
    res=self.fetchData(req,"cloud_agent_service_arguments")
    return res

  ## @brief The tbl cloud_agent_service_arguments write data service callback
  # @param req [rapp_platform_ros_communications::writeDataSrvRequest::Request&] The ROS service request
  # @param res [rapp_platform_ros_communications::writeDataResponse::Response&] The ROS service response
  def tblCloudAgentServiceArgumentsWriteDataHandler(self,req):
    res = writeDataSrvResponse()
    res=self.writeData(req,"cloud_agent_service_arguments")
    return res

  ## @brief The tbl cloud_agent_service_arguments delete data service callback
  # @param req [rapp_platform_ros_communications::deleteDataSrvRequest::Request&] The ROS service request
  # @param res [rapp_platform_ros_communications::deleteDataSrvResponse::Response&] The ROS service response
  def tblCloudAgentServiceArgumentsDeleteDataHandler(self,req):
    res = deleteDataSrvResponse()
    res=self.deleteData(req,"cloud_agent_service_arguments")
    return res

  ## @brief The tbl cloud_agent_service_arguments update data service callback
  # @param req [rapp_platform_ros_communications::updateDataSrvRequest::Request&] The ROS service request
  # @param res [rapp_platform_ros_communications::updateDataSrvResponse::Response&] The ROS service response
  def tblCloudAgentServiceArgumentsUpdateDataHandler(self,req):
    res = updateDataSrvResponse()
    res=self.updateData(req,"cloud_agent_service_arguments")
    return res
