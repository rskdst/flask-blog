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
@index.route("/search/",methods=["get","post"])
def search():
    key_word = request.args.get("keyboard")
    try:
        tag_article_obj_list = Tag.query.filter(Tag.name.like("%" + key_word + "%")).first().article.all()
    except:
        tag_article_obj_list = []
    finally:
        article_obj_list = Article.query.filter(db.or_(
            Article.title.like("%" + key_word + "%"),
            Article.author.like("%" + key_word + "%"),
            Article.description.like("%" + key_word + "%"),
            Article.article_type.like("%" + key_word + "%"),
        )).all()
        article_obj_list += tag_article_obj_list
        data = pagination(article_obj_list)
        return render_template("article.html",**locals())

@index.route("/music/",methods=["get",])
def music():
    return render_template("music.html")