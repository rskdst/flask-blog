from flask import Blueprint
from myblog import models

backstage = Blueprint("backstage",__name__)

@backstage.route("/backstage/",methods=["get",])
def main():
    return render_template("/backstage/index.html")

@backstage.route("/backstage/add_article/",methods=["get","post"])
def add_article():
    if request.method == "GET":
        tag_id = models.Tag.query.all()
        print(tag_id)
        return render_template("/backstage/add_article.html")
    else:
        print(request.form)
        title = request.form.get("title")
        description = request.form.get("description")


        return render_template("/backstage/add_article.html")

@backstage.route("/backstage/article_list/",methods=["get","post"])
def article_list():
    return render_template("/backstage/article_list.html")







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