/*
an easy impl for http to call services in ros
*/
function svcImpl(req, resp, ros) {

  var rosMsg = JSON.parse(req.body.data);
  console.log(req.body);
  rosSrvName = req.body.service;
  // ROS-Service response callback.
  function callback(data) {
    resp.sendJson(data);
  }

  // ROS-Service onerror callback.
  function onerror(e) {
    var response = {}
    response.error = e;
    resp.sendJson(response);
  }

  // Call ROS-Service.
  ros.callService(rosSrvName, rosMsg, {success: callback, fail: onerror});
}

module.exports = svcImpl;
