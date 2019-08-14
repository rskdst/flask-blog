from flask import Blueprint,redirect
from myblog.models import *
from myblog.views.article import pagination
backstage = Blueprint("backstage",__name__)


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
        article_tag = request.form.getlist("article_tag")
        author = request.form.get("author")
        title = request.form.get("title")
        description = request.form.get("description")
        content = request.form.get("content")
        article_type = request.form.get("article_type")
        try:
            article_obj = Article(
                title=title,
                author=author,
                description=description,
                content=content,
                article_type=article_type
            )
            tag_list = [Tag.query.get(int(tag)) for tag in article_tag]
            article_obj.tag = tag_list
            db.session.add_all([article_obj,])
            db.session.commit()
        except Exception as e:
            print(e)
        print(article_tag,author,title,description,content,article_type)
        return render_template("/backstage/add_article.html")


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
    else:
        id = int(request.form.get("article_id"))
        article_tag = request.form.getlist("article_tag")
        author = request.form.get("author")
        title = request.form.get("title")
        description = request.form.get("description")
        content = request.form.get("content")
        article_type = request.form.get("article_type")
        try:
            article_obj = Article.query.get(id)
            article_obj.title = title
            article_obj.author = author
            article_obj.description = description
            article_obj.content = content
            article_obj.article_type = article_type
            article_obj.title = title
            tag_list = [Tag.query.get(int(tag)) for tag in article_tag]
            article_obj.tag = tag_list
            db.session.commit()
        except Exception as e:
            print(e)
        return redirect("/backstage/article_list/")
    return render_template("/backstage/article_detail.html",**params)





# ueditor富文本编辑器配置
from flask import render_template, request
from flask import Response
import datetime
import os


def setImage(image):
    image = image.rsplit(".")
    image_str = image[0]
    time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    new_name = image_str.replace(image_str,"img" + "%s"%time + "." + image[1])
    return new_name


@backstage.route('/pasteimg/', methods=['GET', 'POST'])
def paste_upload():
    if request.method == 'POST':
        image = request.files.get("file")
        print(request.files.get("file"))
        # image_name = setImage(image)
        image_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"../statics/media"))
        image.save(image_path)

        imgdata = request.get_data()
        file = open('test.png', 'wb')
        file.write(imgdata)
        file.close()
    imgsrc = "/static/img/60_1.png"
    return Response(imgsrc, mimetype='application/text')