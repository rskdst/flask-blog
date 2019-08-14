from flask import Blueprint
from flask import Flask,render_template
from myblog.models import *

index = Blueprint("index",__name__)

@index.route("/index/",methods=["get",])
def main():
    tag_id = Tag.query.all()

    return render_template("index.html")

