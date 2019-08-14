from flask import Blueprint,redirect
from myblog.models import *
from myblog.views.article import pagination
backstage = Blueprint("backstage",__name__)

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
        try:
            article_obj = Article.query.get(id)
            article_obj.title = title
            article_obj.author = author
            article_obj.description = description
            article_obj.content = content
            article_obj.article_type = article_type
            article_obj.title = title
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
        try:
            if article_status == "发布文章":
                article_obj = Article(
                    title=title,
                    author=author,
                    description=description,
                    content=content,
                    article_type=article_type,
                    article_status="发布"
                )
            else:
                article_obj = Article(
                    title=title,
                    author=author,
                    description=description,
                    content=content,
                    article_type=article_type,
                    article_status="草稿"
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