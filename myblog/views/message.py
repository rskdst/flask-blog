from flask import Blueprint
from flask import Flask,render_template,request
from myblog.models import LeaveMessage,db
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
        print(data)
        return render_template("message.html",**locals())