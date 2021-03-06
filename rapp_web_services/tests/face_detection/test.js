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


var path = require('path');
var fs = require('fs');

var ENV = require( path.join(__dirname, '../..', 'env.js') );
var INCLUDE_DIR = ENV.PATHS.INCLUDE_DIR;
var Fs = require( path.join(INCLUDE_DIR, 'common', 'fileUtils.js') );
var testParams = require( path.join(__dirname, 'params.json') );


exports.TEST = function (){
  service face_detection();

  var serverCacheDir = ENV.PATHS.SERVER_CACHE_DIR;
  var success = false;
  var response = {};
  var validResponse = testParams.response;
  var args = {};

  for( var arg in testParams.request.args ){
    args[arg] = testParams.request.args[arg];
  }

  args.file_uri = Fs.resolvePath( args.file_uri );

  var fileBasename = path.basename( args.file_uri );
  var destPath = path.join( Fs.resolvePath( serverCacheDir ), fileBasename );


  if( Fs.copyFile(args.file_uri, destPath) ){
    args.file_uri = destPath;
    response = face_detection(args).postSync();

    if(validResponse.error === response.error){
      success = true;
    }
  }

  return {success: success, output: response, input: args};
};

