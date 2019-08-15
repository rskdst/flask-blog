from flask import Blueprint
from flask import Flask,render_template,request
from myblog.models import *
from myblog.views.article import pagination

index = Blueprint("index",__name__)

@index.route("/index/",methods=["get",])
def main():
    article_obj_list = Article.query.filter_by(article_status="发布").order_by(db.desc("created_date")).limit(10).all()
    tag_obj_list = Tag.query.all()
    recommend = Tag.query.filter_by(name="站长推荐").first()
    data = {
        "data_list":article_obj_list,
        "tag_obj_list":tag_obj_list,
        "recommend":recommend
    }
    return render_template("index.html",**locals())


# 搜索
@index.route("/search/",methods=["get",])
def search():
    key_word = request.args.get("key")
    article_obj_list = Article.query.filter_by()