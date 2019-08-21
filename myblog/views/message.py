from flask import Blueprint,redirect
from flask import Flask,render_template,request
from myblog.models import *
from myblog.views.article import pagination

message = Blueprint("message",__name__)



@message.route("/message/",methods=["get","post"])
def main():
    if request.method == "GET":
        message_list = []
        leave_message_obj_list = LeaveMessage.query.order_by(db.desc("created_date")).all()
        for leave_message_obj in leave_message_obj_list:
            message_dict = {}
            if leave_message_obj.reply_id == None:
                message_dict["message"] = leave_message_obj
                message_dict["reply"] = LeaveMessage.query.filter_by(reply_id=leave_message_obj.id).first()
                message_list.append(message_dict)
        data = pagination(message_list)
        type_obj_list = Type.query.all()
        hot_article_list = Article.query.order_by("article_praise").limit(5).values(Article.id, Article.title,Article.article_picture)  # 热门文章列表
        return render_template("message.html",**locals())
    else:
        username = request.form.get("username")
        email = request.form.get("email")
        content = request.form.get("content")
        if not User.query.filter_by(username=username).first():
            user = User(username=username, email=email)
            db.session.add(user)
            db.session.commit()
        user_id = User.query.filter_by(username=username).first().id
        leave_message_obj = LeaveMessage(
            user_id=user_id,
            content=content
        )
        db.session.add(leave_message_obj)
        db.session.commit()
        return redirect("/message/")