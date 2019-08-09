from flask import Blueprint
from flask import Flask,render_template,request
from myblog.models import *

article = Blueprint("article",__name__)


# 分页功能
def pagination():
    pass


# 文章首页
@article.route("/article/",methods=["get",])
def main():
    article_obj_list = Article.query.order_by(db.desc("created_date"))
    tag_obj_list = Tag.query.all()
    recommmend = Tag.query.filter_by(name="站长推荐").all()
    return render_template("article.html",**locals())

# 文章详情页
@article.route("/detail/",methods=["get","post"])
def detail():
    tag_obj_list = Tag.query.all()
    article_id = request.args.get("article_id")
    article_obj = Article.query.get(article_id)
    return render_template("article_content.html",**locals())

# 文章分类页
@article.route("/article/type/",methods=["get","post"])
def article_type():
    tag_id = int(request.args.get("tag_id"))
    tag_obj = Tag.query.get(tag_id)
    article_obj_list = tag_obj.article
    tag_obj_list = Tag.query.all()
    recommmend = Tag.query.filter_by(name="站长推荐").all()
    return render_template("article.html",**locals())