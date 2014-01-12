import SocketServer
import os.path
# coding: utf-8

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

mime = {"html":" text/html\n\n",
        "css":" text/css\n\n"}

status = {"200":" 200 OK\n",
        "415":" 415 Unsupported Media Type\n",
        "400":" 404 Not Found\n"}

rootPath = "./www"

class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        data = self.request.recv(1024).strip()
        methodStr = data.split()[0]
        # Get the method from the request
        httpVer = data.split()[2]
        # Get the http protocl version
        filePath = data.split()[1]
        # Get directory of the target file

        if os.path.isfile(rootPath + filePath):
        # test if the file exists
            fileExt = filePath.split(".")[1]
            if (fileExt == 'css') or (fileExt == 'html') :
                # open a file in either .css or .html type
                f = open(rootPath + filePath,'r')

                content = ( httpVer + status["200"] + "Content-Type:" + mime[fileExt]
                        + f.read())
            else:

                content = ( httpVer + status["415"] +
                        "Content-Type:" + mime["html"] +
                        "<!DOCTYPE html>\n"+
                        "<html><body>" + httpVer + ' 415 Unsupported Media Type\n'+
                        "</body></html>" )

        elif filePath == "/":
        # when path is /
            if os.path.isfile(rootPath + "/index.html"):
               
                f = open(rootPath + "/index.html",'r')
                content = ( httpVer + status["200"] +
                    "Content-Type:" + mime["html"] +
                    f.read())

        else:
            content = ( httpVer + status["400"] +
            "Content-Type:" + mime["html"]+
            "<!DOCTYPE html>\n" +
            "<html><body>" + httpVer + status["400"] +
            "</body></html>")
             
        self.request.sendall(content)

               
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

