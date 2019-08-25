from flask import Blueprint
from flask import Flask,render_template,request,jsonify,redirect
from myblog.models import *
from myblog.views.article import pagination

index = Blueprint("index",__name__)

@index.route("/index/",methods=["get",])
def main():
    article_obj_list = Article.query.filter_by(article_status="发布").order_by(db.desc("created_date")).all() # 首页文章列表
    sum_page = len([i + 1 for i in range((len(list(article_obj_list)) + 7 - 1) // 7)])
    print(sum_page)
    article_obj_list = article_obj_list[0:7]
    praise_show_list = Article.query.order_by("article_praise").limit(4).values(Article.id,Article.title,Article.article_picture,Article.description) # 轮播图文章列表
    hot_article_list = Article.query.order_by("article_praise").limit(5).values(Article.id,Article.title,Article.article_picture) # 热门文章列表
    type_obj_list = Type.query.all() # 文章类型列表
    recommend = Tag.query.filter_by(name="站长推荐").first() # 站长推荐列表
    tag_obj_list = Tag.query.all()
    return render_template("index.html",**locals())


# 搜索
@index.route("/search/",methods=["get","post"])
def search():
    key_word = request.args.get("keyboard")
    try:
        type_article_obj_list = Type.query.filter(Type.name.like("%" + key_word + "%")).first().article.all()
    except:
        type_article_obj_list = []
    finally:
        article_obj_list = Article.query.filter(db.or_(
            Article.title.like("%" + key_word + "%"),
            Article.author.like("%" + key_word + "%"),
            Article.description.like("%" + key_word + "%"),
            Article.article_type.like("%" + key_word + "%"),
        )).all()
        article_obj_list += type_article_obj_list
        data = pagination(article_obj_list)
        type_obj_list = Type.query.all()
        tag_obj_list = Tag.query.all()
        return render_template("article.html",**locals())




# 音乐
@index.route("/music/",methods=["get","post"])
def music():
    if request.method == "GET":
        type_obj_list = Type.query.all()
        return render_template("music.html", **locals())
    else:
        music_obj_list = Music.query.all()
        music_list = []
        for music_obj in music_obj_list:
            dict = {}
            dict["title"] = music_obj.title
            dict["singer"] = music_obj.singer
            dict["image"] = music_obj.image
            dict["src"] = music_obj.src
            music_list.append(dict)
        return jsonify(music_list)

# 增加赞数
@index.route("/add_praise/",methods=["get","post"])
def add_praise():
    if request.args.get("article_praise"):
        id = request.args.get("id")
        article_praise = int(request.args.get("article_praise"))+1
        Article.query.filter_by(id=id).update({"article_praise":article_praise})
        db.session.commit()
        return "保存成功"
    else:
        id = request.args.get("id")
        article_praise = int(request.args.get("praise")) + 1
        Article.query.filter_by(id=id).update({"article_praise": article_praise})
        db.session.commit()
        return redirect("/detail/?article_id={}".format(id))



# 关于我
@index.route("/aboutme/",methods=["get","post"])
def about_me():
    return render_template("aboutme.html",**locals())






































