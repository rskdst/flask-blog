from flask import Blueprint
from flask import Flask,render_template

message = Blueprint("message",__name__)

@message.route("/message/",methods=["get",])
def main():
    return render_template("message.html")