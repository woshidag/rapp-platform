/*!
 * @file storeFile_test.js
 * @brief Test filetransfer methods from local to host.
 */

var user = process.env.LOGNAME;
var rapp_hop_path = "/home/" + user + "/Desktop/rapp-platform-catkin-ws/src/rapp-platform/ric/hop_services/";
var rel_rappPath = "~/Desktop/rapp-platform-catkin-ws/src/rapp-platform/ric/hop_services/"
var filePath = rel_rappPath + "tests/auxiliary/Robot_Blue.jpg";
var destPath = "~/hop_temps/test.jpg"

var HopUtils = require(rapp_hop_path + "utilities/./HopServiceUtils.js");
var ServerParams = require(rapp_hop_path + "utilities/./ServerParams.js");


var params = new ServerParams(false, "155.207.19.37", 9001, "rappdev", "rappdev");
var hsu = new HopUtils();
//hsu.init(params);
var size = hsu.sendFile( filePath, destPath, params );
console.log( size );


