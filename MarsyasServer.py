#!/usr/bin/env python

from marsyas import *
from marsyas_util import *
import os
from flask import Flask, render_template, request, redirect, url_for, session
import yaml

app = Flask(__name__)
app.debug = True
app.secret_key = os.environ['KEY']

global_net = "1" #sessions do not support the storage of objects, thus resort to use global variables in a server instance
@app.route("/InitNet", methods=['POST'])
def InitNet():
    try:
        netSpec = yaml.safe_load(request.data)['netDef'] #Using yaml.safe_load to unpack json since it will maintain the type of the input from client rather than re-encoding itself through json.loads()
        global global_net
        global_net = create(netSpec)
        return "Network Created"
    except(error):
        print error
        raise NetworkNotCreated

@app.route("/LinkCtrl", methods=['POST'])
def LinkCtrl():
    try:
        data = yaml.safe_load(request.data)
        dest = str(data['dest'])
        mrs_type = str(data['mrs_type'])
        global_net.linkControl(dest, mrs_type)
        return "Link Control added"
    except(error):
        print error
        raise NetworkNotCreated

@app.route("/UpdateCtrl", methods=['POST'])
def UpdateCtrl():
    try:
        data = yaml.safe_load(request.data)
        dest_key = str(data['dest_key'])
        dest_value = str(data['dest_value'])
        global_net.updControl(dest_key, dest_value)
        return "Link Control added"
    except(error):
        print error
        raise NetworkNotCreated

@app.route("/GetCtrl", methods=['POST'])
def GetCtrl():
    try:
        data = yaml.safe_load(request.data)
        dest_key = str(data['dest_key'])
        output = global_net.getControl(dest_key)
        print output
        return "output"
        #return output
    except(error):
        print error
        raise NetworkNotCreated

@app.route("/GetNET", methods=['POST'])
def GetNET():
    try:
        print global_net
        return global_net
    except(error):
        print error
        raise NetworkNotCreated

@app.errorhandler("NetworkNotCreated")
def handle_error_networknotcreated(error):
    print "NNC"
    return {'message': error.message}, 400

if __name__ == "__main__":
    app.run()
