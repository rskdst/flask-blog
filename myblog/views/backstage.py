
from flask import Blueprint,redirect,request,render_template
from myblog.models import *
from werkzeug.utils import secure_filename
from myblog.views.article import pagination
import os

backstage = Blueprint("backstage",__name__)

# 评论留言分类
def comment_pagination(all_data):
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
    return locals()



# 图片上传
def up_picture(image_obj):
    image = image_obj.filename
    image = image.rsplit(".")
    image_str = image[0]
    time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    picture_name = image_str.replace(image_str,"img" + "%s"%time + "." + image[1])
    image_obj.filename = picture_name
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../statics/images"))
    upload_path = os.path.join(base_path, "article_picture",secure_filename(image_obj.filename))
    image_obj.save(upload_path)
    return picture_name

# 保存文章
def save_article(request):
    article_tag = request.form.getlist("article_tag")
    author = request.form.get("author")
    title = request.form.get("title")
    description = request.form.get("description")
    content = request.form.get("content")
    article_type = request.form.get("article_type")
    article_status = request.form.get("submit")
    if request.form.get("article_id"):
        id = int(request.form.get("article_id"))
        image_obj = request.files.get("article_picture")
        try:
            article_obj = Article.query.get(id)
            article_obj.title = title
            article_obj.author = author
            article_obj.description = description
            article_obj.content = content
            article_obj.article_type = article_type
            article_obj.title = title
            if image_obj:
                picture_name = up_picture(image_obj)
                article_obj.article_picture = picture_name
            else:
                pass
            if article_status == "发布文章":
                article_obj.article_status = "发布"
            else:
                article_obj.article_status = "草稿"
            tag_list = [Tag.query.get(int(tag)) for tag in article_tag]
            article_obj.tag = tag_list
            db.session.commit()
        except Exception as e:
            print(e)
    else:
        image_obj = request.files.get("article_picture")
        if image_obj:
            picture_name = up_picture(image_obj)
        else:
            picture_name = None
        try:
            if article_status == "发布文章":
                article_obj = Article(
                    title=title,
                    author=author,
                    description=description,
                    content=content,
                    article_type=article_type,
                    article_status="发布",
                    article_picture=picture_name
                )
            else:
                article_obj = Article(
                    title=title,
                    author=author,
                    description=description,
                    content=content,
                    article_type=article_type,
                    article_status="草稿",
                    article_picture=picture_name
                )
            tag_list = [Tag.query.get(int(tag)) for tag in article_tag]
            article_obj.tag = tag_list
            db.session.add_all([article_obj, ])
            db.session.commit()
        except Exception as e:
            print(e)
    data = {
        "title":title,
        "description":description,
        "article_status":article_status

    }
    return data


@backstage.route("/backstage/",methods=["get",])
def main():
    return render_template("/backstage/index.html")


# 添加文章
@backstage.route("/backstage/add_article/",methods=["get","post"])
def add_article():
    if request.method == "GET":
        tag_obj_list = Tag.query.all()
        return render_template("/backstage/add_article.html",**{"tag_obj_list":tag_obj_list})
    else:

        if request.form.get("submit") == "发布文章":
            data = save_article(request)
            return render_template("/backstage/article_result.html", **locals())
        elif request.form.get("submit") == "保存为草稿":
            data = save_article(request)
            return render_template("/backstage/article_result.html", **locals())
        else:
            return redirect("/backstage/article_list/")




# 文章列表页
@backstage.route("/backstage/article_list/",methods=["get","post"])
def article_list():
    article_obj_list = Article.query.order_by(db.desc("created_date")).all()
    data = pagination(article_obj_list)
    return render_template("/backstage/article_list.html",**locals())


# 文章详情页
@backstage.route("/backstage/article_detail/",methods=["get","post"])
def article_detail():
    if request.method == "GET":
        tag_obj_list = Tag.query.all()
        id = int(request.args.get("id"))
        article_obj = Article.query.get(id)
        params = {
            "article_obj": article_obj,
            "tag_obj_list":tag_obj_list
        }
        return render_template("/backstage/article_detail.html", **params)
    else:
        if request.form.get("submit") == "发布文章":
            data = save_article(request)
            return render_template("/backstage/article_result.html", **locals())
        elif request.form.get("submit") == "保存为草稿":
            data = save_article(request)
            return render_template("/backstage/article_result.html", **locals())
        elif request.form.get("submit") == "返回":
            return redirect("/backstage/article_list/")
        else:
            id = int(request.form.get("article_id"))
            article = Article.query.filter(Article.id==id).first()
            Comment.query.filter(Comment.article_id==id).delete(synchronize_session=False)
            db.session.delete(article)
            db.session.commit()
            data = {
                "title": article.title,
                "description": article.description,
                "article_status": "删除"
            }

            return render_template("/backstage/article_result.html",**locals())


# 留言管理
@backstage.route("/manage/message/",methods=["get","post"])
def message_manage():
    if request.method == "GET":
        message_list = []
        leave_message_obj_list = LeaveMessage.query.order_by(db.desc("created_date")).all()
        for leave_message_obj in leave_message_obj_list:
            message_dict = {}
            if leave_message_obj.reply_id == None:
                message_dict["message"] = leave_message_obj
                message_dict["reply"] = LeaveMessage.query.filter_by(reply_id=leave_message_obj.id).first()
                message_list.append(message_dict)
        data = comment_pagination(message_list)
        return render_template("/backstage/message_manage.html", **locals())
    else:
        if request.form.get("submit") == "回复":
            reply_id = request.form.get("message_id")
            user_id = 1
            content = request.form.get("reply")
            leave_message_obj = LeaveMessage(
                user_id=user_id,
                reply_id=reply_id,
                content=content
            )
            db.session.add(leave_message_obj)
            db.session.commit()
        elif request.form.get("submit") == "删除1":
            if request.form.get("reply_id"):
                message_id = request.form.get("message_id")
                reply_id = request.form.get("reply_id")
                LeaveMessage.query.filter_by(id=message_id).delete(synchronize_session=False)
                LeaveMessage.query.filter_by(id=reply_id).delete(synchronize_session=False)
                db.session.commit()
            else:
                message_id = request.form.get("message_id")
                LeaveMessage.query.filter_by(id=message_id).delete(synchronize_session=False)
                db.session.commit()
        else:
            reply_id = request.form.get("reply_id")
            LeaveMessage.query.filter_by(id=reply_id).delete(synchronize_session=False)
            db.session.commit()
        return redirect(request.headers.get("Referer"))


# 评论管理
@backstage.route("/manage/comment/",methods=["get","post"])
def comment_manage():
    if request.method == "GET":
        all_article_id = Article.query.with_entities(Article.id,Article.title).all()
        comments_list = []
        for article_id_tuple in all_article_id:
            article_id = article_id_tuple[0]
            article_title = article_id_tuple[1]
            comment_obj_list = Comment.query.filter_by(article_id=article_id).order_by(db.desc("created_date")).all()
            comment_list = []
            for comment_obj in comment_obj_list:
                comment_dict = {}
                if comment_obj.parent_id == None:
                    parent_dict = {}
                    parent_dict["id"] = comment_obj.id
                    parent_dict["user_id"] = comment_obj.user_id
                    parent_dict["username"] = comment_obj.user_comment.username
                    parent_dict["parent_id"] = comment_obj.parent_id
                    parent_dict["reply_comment_id"] = comment_obj.reply_comment_id
                    parent_dict["article_id"] = article_id
                    parent_dict["reply_id"] = comment_obj.user_comment.id
                    parent_dict["content"] = comment_obj.content
                    parent_dict["created_date"] = str(comment_obj.created_date)
                    comment_dict["parent_comment"] = parent_dict
                    son_comment_list = [son_comment for son_comment in comment_obj_list if
                                        son_comment.parent_id == comment_obj.id]
                    son_list = []
                    for son_comment in son_comment_list:
                        son_dict = {}
                        son_dict["id"] = son_comment.id
                        son_dict["user_id"] = son_comment.user_id
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
            comments_tuple = (article_id,article_title,comment_list)
            comments_list.append(comments_tuple)
        data = comment_pagination(comments_list)
        return render_template("/backstage/comment_manage.html",**locals())

    else:
        if request.form.get("submit") == "回复":
            parent_id = request.form.get("parent_id")
            article_id = request.form.get("article_id")
            reply_id = request.form.get("reply_id")
            content = request.form.get("content")
            comment_obj = Comment(
                user_id=1,
                parent_id=parent_id,
                article_id=article_id,
                reply_id=reply_id,
                content=content
            )
            db.session.add(comment_obj)
            db.session.commit()
        else:
            print(request.headers)
            if request.form.get("parent_comment"):
                comment_id = request.form.get("parent_comment")
                Comment.query.filter_by(id=comment_id).delete(synchronize_session=False)
                Comment.query.filter_by(parent_id=comment_id).delete(synchronize_session=False)
                db.session.commit()
            else:
                comment_id = request.form.get("son_comment")
                parent_id = request.form.get("parent_id")
                Comment.query.filter_by(id=comment_id).delete(synchronize_session=False)
                Comment.query.filter(db.and_(Comment.parent_id==parent_id,Comment.reply_comment_id==comment_id)).delete(synchronize_session=False)
                db.session.commit()
        return redirect(request.headers.get("Referer"))


# 添加音乐
@backstage.route("/backstage/add_music/",methods=["get","post"])
def add_music():
    if request.method == "GET":
        return render_template("/backstage/add_music.html")
    else:
        title = request.form.get("title")
        singer = request.form.get("singer")
        image_obj = request.files.get("image")
        music_obj = request.files.get("music")
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../statics/music"))
        image_upload_path = os.path.join(base_path, "images", secure_filename(image_obj.filename))
        image_obj.save(image_upload_path)
        music_upload_path = os.path.join(base_path, "music", secure_filename(music_obj.filename))
        music_obj.save(music_upload_path)
        music_obj = Music(
            title=title,
            singer=singer,
            image=image_obj.filename,
            src=music_obj.filename
        )
        db.session.add(music_obj)
        db.session.commit()
        return render_template("/backstage/add_music.html")


# 编辑音乐
@backstage.route("/backstage/music_list/",methods=["get","post"])
def editor_music():
    if request.method == "GET":
        music_obj_list = Music.query.all()
        data = comment_pagination(music_obj_list)
        return render_template("/backstage/music_list.html",**locals())
    else:
        print(request.form)
        id = request.form.get("id")
        image = request.form.get("image")
        src = request.form.get("music")

        Music.query.filter_by(id=id).delete(synchronize_session=False)
        db.session.commit()
        image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../statics/music/images/{}".format(image)))
        os.remove(image_path)
        music_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../statics/music/music/{}".format(src)))
        os.remove(music_path)
        return redirect("/backstage/music_list/")
































