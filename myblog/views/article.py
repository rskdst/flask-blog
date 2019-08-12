from flask import Blueprint
from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api,Resource
from myblog.models import *

article = Blueprint("article",__name__)
api = Api(article)


# 分页功能
def pagination(all_data):
    try:
        current_page = int(request.args.get("page", 1))
    except:
        current_page = 1
    page_range = [i + 1 for i in range((len(list(all_data)) + 7 - 1) // 7)]
    if current_page not in page_range:
        current_page = 1
    next_page = current_page + 1
    if next_page not in page_range:
        next_page = None
    pre_page = current_page - 1
    if pre_page not in page_range:
        pre_page = None
    start = (current_page - 1) * 7
    end = current_page * 7
    article_obj_list = all_data[start:end]
    tag_obj_list = Tag.query.all()
    recommend = Tag.query.filter_by(name="站长推荐").first()
    return locals()


# 文章首页
@article.route("/article/",methods=["get",])
def main():
    all_article_obj_list = Article.query.order_by(db.desc("created_date")).all()
    data = pagination(all_article_obj_list)
    return render_template("article.html",**locals())

# 文章详情页
@article.route("/detail/",methods=["get","post"])
def detail():
    tag_obj_list = Tag.query.all()
    article_id = request.args.get("article_id")
    article_obj = Article.query.get(article_id)
    recommend = Tag.query.filter_by(name="站长推荐").first()
    return render_template("article_content.html",**locals())

# 文章分类页
@article.route("/article/type/",methods=["get","post"])
def article_type():
    tag_id = int(request.args.get("tag_id"))
    tag_obj = Tag.query.get(tag_id)
    all_article_obj_list = tag_obj.article
    data = pagination(all_article_obj_list)

    return render_template("article.html",**locals())


# 文章评论
class _Comment(Resource):
    def get(self):
        article_id = int(request.args.get("params[article_id]"))
        data = {}
        comment_obj_list = Comment.query.filter(article_id==article_id).all()
        comment_list = []
        for comment_obj in comment_obj_list:
            comment_dict = {}
            if comment_obj.parent_id == None:
                parent_dict = {}
                parent_dict["username"] = comment_obj.user_comment.username
                if comment_obj.parent_comment:
                    parent_dict["parent"] = comment_obj.parent_comment.username
                else:
                    parent_dict["parent"] = comment_obj.parent_comment
                parent_dict["article_id"] = article_id
                parent_dict["reply_id"] = comment_obj.reply_id
                parent_dict["content"] = comment_obj.content
                parent_dict["created_date"] = str(comment_obj.created_date)
                comment_dict["parent_comment"] = parent_dict
                son_comment_list = [son_comment for son_comment in comment_obj_list if son_comment.parent_id == comment_obj.id]
                print(son_comment_list)
                son_list = []
                for son_comment in son_comment_list:
                    son_dict = {}
                    son_dict["username"] = son_comment.user_comment.username
                    son_dict["parent"] = son_comment.parent_comment.username
                    son_dict["article_id"] = article_id
                    son_dict["reply_id"] = son_comment.reply_id
                    son_dict["content"] = son_comment.content
                    son_dict["created_date"] = str(son_comment.created_date)
                    son_list.append(son_dict)
                comment_dict["son_comment"] = son_list
            if comment_dict:
                comment_list.append(comment_dict)

        data["data"] = comment_list
        return data

    def post(self):
        return {"hello":"HelloWorld"}

api.add_resource(_Comment,"/article/api/comment/")