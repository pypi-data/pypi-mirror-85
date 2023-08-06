#!/usr/bin/python

# SQLMorph API CLI Tool is licensed under the following terms:
#
#    Copyright 2020, phData, Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import os
import sys
import getopt
import argparse
import urllib.request as request
import urllib.parse as parse
import json
import time

def createFiles(results, inputDir, target):
    for result in results:
        filepath, filename = calculateOutputFile(result["name"], inputDir, target)
        
        if not os.path.exists(filepath):
            sys.stderr.write('Creating directory: %s\n' % filepath)
            os.makedirs(filepath)

        with open(os.path.join(filepath, filename), 'wb') as temp_file:
            sys.stderr.write('Writing results to: %s%s\n' % (filepath, filename))
            temp_file.write('\n'.join(result["result"]).encode())

def calculateOutputFile(name, inputDir, target):
    fixedInput = inputDir.strip("/")
    directory = "%s.%s/" % (fixedInput, target)
    length = len(fixedInput)+1
    filename = name.split('/')[-1:][0]
    filepath = directory + name[length:-len(filename)]
    return filepath, filename

def readFile(path):
    result = {}
    with open(path, "r") as myFile:
        result = { "name": path, "contents": myFile.read()}
    return result

def readDirectory(path):
    contents = []
    count = 1
    totalCount = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            totalCount += 1
    for root, dirs, files in os.walk(path):
        for file in files:
            fileContents = readFile(os.path.join(root, file))
            contents.append({**fileContents, "number": "%s/%s" % (count, totalCount)})
            count += 1
    return contents

def makeRequests(baseUrl, files, source, target, authentication, inputDir):
    requests = []
    for myFile in files:
        if inputDir:
            filepath, filename = calculateOutputFile(myFile["name"], inputDir, target)
            outputFile = os.path.join(filepath, filename)
            if os.path.isfile(outputFile) and os.path.getsize(outputFile) > 0:
                sys.stderr.write("Skipping file due to existing output: %s (%s)\n" % (myFile["name"], myFile.get("number", "1/1")))
                continue

        sys.stderr.write("Queueing file: %s (%s)\n" % (myFile["name"], myFile.get("number", "1/1")))
        body = {
            "source": source,
            "target": target,
            "statement": myFile['contents']
        }
        
        auth_header = "BEARER %s" % authentication
        headers = {
            "Authorization": auth_header,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        data = json.dumps(body).encode('utf-8')

        myRequest = request.Request(baseUrl + "/api/v3/convert", data=data, headers=headers)
        requests.append({"file": myFile, "request": myRequest})

    responses = handleRequestQueue(requests)
    return responses

def handleRequestQueue(requests):
    localRequests = requests
    responses = []

    while localRequests:
        myRequest = localRequests.pop(0)
        myFile = myRequest["file"]
        sys.stderr.write("Sending request to server for file: %s (%s)\n" % (myFile["name"], myFile.get("number", "1/1")))
        try:
            response = request.urlopen(myRequest["request"])
            id = response.read().decode('utf-8')
            responses.append({**myFile, "id": id})
        except Exception as e:
            if 'HTTP Error 401' in str(e):
                print("Invalid Auth Token")
                sys.exit(2)
            else:
                sys.stderr.write("%s\n" % e)
                time.sleep(0.25)
            localRequests.append(myRequest)
            continue
    return responses

def handleResponses(baseUrl, responses, authentication, inputDir, target):
    responsesToProcess = responses
    errors = []
    while responsesToProcess:
        responseToProcess = responsesToProcess.pop(0)
        auth_header = "BEARER %s" % authentication
        headers = {
            "Authorization": auth_header,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        myRequest = request.Request(baseUrl + "/api/v3/convert/" + responseToProcess['id'], headers=headers)
        try:
            response = request.urlopen(myRequest)
        except Exception as e:
            if 'HTTP Error 401' in str(e):
                print("Invalid Auth Token")
                sys.exit(2)
            else:
                sys.stderr.write("%s\n" % e)
                responseToProcess.append(responseToProcess)
                time.sleep(0.25)
            continue
        code = response.getcode()

        # if the sql hasn't finished processing, go to the next one and put back in list
        if code == 202:
            responsesToProcess.append(responseToProcess)
            continue

        #decode response and write to file
        responseData = json.loads(response.read().decode('utf-8'))
        queries = []
        for data in responseData:
            if data["translateCompilation"]["error"] is not None:
                print(responseToProcess["name"])
                sys.stderr.write("ERROR in file: %s\n" % responseToProcess["name"])
                sys.stderr.write("%s\n" % data["translateCompilation"]["error"])
                errors.append({"name": responseToProcess["name"], "error": data["translateCompilation"]["error"]})
            else:
                queries.append(data["targetStmt"])
        sys.stderr.write("Finished processing file: %s (%s)\n" % (responseToProcess["name"], responseToProcess.get("number","1/1")))
        result = {**responseToProcess, "result": queries}
        if not inputDir:
            print('\n'.join(result["result"]))
        else:
            createFiles([result], inputDir, target)
    return errors

def printErrors(errors):
    if errors:
        for error in errors:
            print("Error in file: %s\nReason: %s\n" % (error["name"], error["error"]))

def runner(runnerArgs):
    startApp = time.time()
    parser = argparse.ArgumentParser(prog='sqlmorph_api.py', description="Utility for scripting access to the SQLMorph Api")
    parser.add_argument('--url', required=False, type=str, help="SQLMorph API Url", dest="url", default="https://sqlmorph.customer.phdata.io:443/")
    requiredParams = parser.add_argument_group("required arguments")
    requiredParams.add_argument('--source', required=True, type=str, help="Source dialect", choices=["mssql", "hana", "teradata", "oracle", "impala", "netezza", "snowflake"], dest="source")
    requiredParams.add_argument('--target', required=True, type=str, help="Target dialect", choices=["impala", "snowflake", "hana", "oracle"], dest="target")
    requiredParams.add_argument('--auth-token', required=True, type=str, help="Okta Access Token", dest="auth")
    requiredParams.add_argument('--input', required=True, type=str, help="File or directory to translate", dest="input")
    args = parser.parse_args(runnerArgs);
    sys.stderr.write('\n')
    baseUrl = args.url.strip("/")

    startFileRead = time.time()
    files = []
    isDir = False
    inputDir = None
    if os.path.isdir(args.input):  
        isDir = True
        files.extend(readDirectory(args.input))
        inputDir = args.input
    elif os.path.isfile(args.input):
        files.append(readFile(args.input))
    else:
        sys.stderr.write("Input is neither a directory or a file.  Exiting.\n")
        sys.exit(1)
        
    endFileRead = time.time()

    startRequests = time.time()
    responses = makeRequests(baseUrl, files, args.source, args.target, args.auth, inputDir)
    endRequests = time.time()
    startResponses = time.time()
    errors = handleResponses(baseUrl, responses, args.auth, inputDir, args.target)
    endResponses = time.time()

    endApp = time.time()
    printErrors(errors)
    sys.stderr.write("\nTotal files: %d\n" % len(files))
    sys.stderr.write("Total script run time: %.2fs\n" % (endApp-startApp))
    sys.stderr.write("Total request time: %.2fs\n" % (endRequests-startRequests))
    sys.stderr.write("Total response retrieval time: %.2fs\n" % (endResponses-startResponses))

def main():
    runner(sys.argv[1:])

if __name__ == "__main__":
    main()
