from flask import Blueprint
from flask import Flask,render_template,request,redirect
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
    data_list = all_data[start:end]
    tag_obj_list = Tag.query.all()
    recommend = Tag.query.filter_by(name="站长推荐").first()
    return locals()


# 文章首页
@article.route("/article/",methods=["get",])
def main():
    all_article_obj_list = Article.query.filter_by(article_status="发布").order_by(db.desc("created_date")).all()
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
    all_article_obj_list = tag_obj.article.filter_by(article_status="发布").order_by(db.desc("created_date")).all()
    data = pagination(all_article_obj_list)

    return render_template("article.html",**locals())


# 文章评论
@article.route("/article/comment/",methods=["get","post"])
def add_comment():
    print(request.form)
    username = request.form.get("username")
    email = request.form.get("email")
    content = request.form.get("content")
    article_id = request.form.get("article_id")
    reply_comment_id = request.form.get("reply_comment_id")
    parent_id = request.form.get("parent_id")
    reply_id = request.form.get("reply_id")
    if not User.query.filter(username==username):
        user = User(username=username,email=email)
        db.session.add(user)
        db.session.commit()
    user_id = User.query.filter_by(username=username).first().id
    if parent_id:
        comment = Comment(
            user_id=user_id,
            parent_id=parent_id,
            article_id=article_id,
            reply_comment_id=reply_comment_id,
            reply_id=reply_id,
            content=content
        )
        db.session.add(comment)
        db.session.commit()
    else:
        comment = Comment(
            user_id=user_id,
            article_id=article_id,
            content=content
        )
        db.session.add(comment)
        db.session.commit()
    return redirect("/detail/?article_id={}/#article_conmment".format(article_id))

# 评论模块
class _Comment(Resource):
    def get(self):
        article_id = int(request.args.get("params[article_id]"))
        data = {}
        comment_obj_list = Comment.query.filter_by(article_id=article_id).order_by(db.desc("created_date")).all()
        comment_list = []
        for comment_obj in comment_obj_list:
            comment_dict = {}
            if comment_obj.parent_id == None:
                parent_dict = {}
                parent_dict["id"] = comment_obj.id
                parent_dict["username"] = comment_obj.user_comment.username
                parent_dict["parent_id"] = comment_obj.parent_id
                parent_dict["reply_comment_id"] = comment_obj.reply_comment_id
                parent_dict["article_id"] = article_id
                parent_dict["reply_id"] = comment_obj.user_comment.id
                parent_dict["content"] = comment_obj.content
                parent_dict["created_date"] = str(comment_obj.created_date)
                comment_dict["parent_comment"] = parent_dict
                son_comment_list = [son_comment for son_comment in comment_obj_list if son_comment.parent_id == comment_obj.id]
                son_list = []
                for son_comment in son_comment_list:
                    son_dict = {}
                    son_dict["id"] = son_comment.id
                    son_dict["username"] = son_comment.user_comment.username
                    son_dict["parent"] = son_comment.reply_comment.username
                    son_dict["parent_id"] = son_comment.parent_id
                    son_dict["reply_comment_id"] = son_comment.reply_comment_id
                    son_dict["article_id"] = article_id
                    son_dict["reply_id"] = son_comment.user_comment.id
                    son_dict["content"] = son_comment.content
                    son_dict["created_date"] = str(son_comment.created_date)
                    son_list.append(son_dict)
                son_list.reverse()
                comment_dict["son_comment"] = son_list
            if comment_dict:
                comment_list.append(comment_dict)
        data["data"] = comment_list
        print(data)
        return data

    def post(self):
        return {"hello":"HelloWorld"}

api.add_resource(_Comment,"/article/api/comment/")