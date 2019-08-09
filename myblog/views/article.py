from flask import Blueprint
from flask import Flask,render_template

article = Blueprint("article",__name__)

@article.route("/article/",methods=["get",])
def main():
    return render_template("article.html")