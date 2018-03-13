from flask import Flask
from flask import jsonify
from flask import request

from db import *

app = Flask(__name__)

db = DBEngine()
print(db.get_stat())

@app.route("/api", methods=['GET'])
def info():
    return "<h3>devils {0[0]}</h3> <br>AND <br><h3>not devils: {0[1]}</h3>".format(db.get_stat())

@app.route("/api/stat", methods=['GET'])
def stat():
    resp = {
               "devil": db.get_stat()[0],
               "notdevil": db.get_stat()[1]
           }
    return jsonify(resp)

@app.route("/api/devil", methods=['GET'])
def deveil_add():
    ip = Ip(request.headers["X-Real-Ip"], request.headers["X-Time"])
    if db.check_ip(ip):
        votes = Votes(1, db.get_stat()[0] + 1, db.get_stat()[1])
        db.save(votes)
    return stat()

@app.route("/api/notdevil", methods=['GET'])
def notdevil_add():
    ip = Ip(request.headers["X-Real-Ip"], request.headers["X-Time"])
    if db.check_ip(ip):
        votes = Votes(1, db.get_stat()[0], db.get_stat()[1] + 1)
        db.save(votes)
    return stat()

@app.route("/api/ip", methods=['GET'])
def ip():
    return jsonify(dict(request.headers.items()))

@app.route("/api/ips", methods=['GET'])
def ip_list():
    resp = {}
    for ip in db.get_ips():
        resp[ip.ip] = ip.date
    return jsonify(resp)
