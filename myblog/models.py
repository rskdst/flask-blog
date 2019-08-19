from myblog import db

import datetime


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)


Article_Tag = db.Table(
    "article_tag",
    db.Column("id",db.Integer,primary_key=True,autoincrement=True),
    db.Column("article_id",db.Integer,db.ForeignKey("article.id")),
    db.Column("tag_id",db.Integer,db.ForeignKey("tag.id"))

)

# 文章
class Article(BaseModel):
    __tablename__ = "article"
    title = db.Column(db.String(100)) # 文章标题
    author = db.Column(db.String(20)) # 文章作者
    created_date = db.Column(db.DateTime, default=datetime.datetime.now) # 文章创建日期
    update_date = db.Column(db.DateTime, nullable=False,default=datetime.datetime.now,onupdate=datetime.datetime.now) # 文章更新日期
    description = db.Column(db.String(200)) # 文章描述
    content = db.Column(db.Text) # 文章内容
    article_type = db.Column(db.String(3)) # 文章类型
    article_status = db.Column(db.String(10)) # 文章状态
    article_picture = db.Column(db.String(100)) # 文章图片
    article_browse = db.Column(db.Integer,default=10) # 文章浏览量
    article_praise = db.Column(db.Integer,default=1) # 文章点赞数

    tag = db.relationship("Tag",
        secondary=Article_Tag,
        lazy='dynamic',
        backref=db.backref('article',lazy="dynamic") # 多对多时想让反向查询查询也显示查询语句要这样写
    )
    comment = db.relationship(
        "Comment",
        lazy='dynamic',
        backref="article",
    )


# 文章标签
class Tag(BaseModel):
    __tablename__ = "tag"
    name = db.Column(db.String(32), unique=True)


# 文章评论
class Comment(BaseModel):
    __tablename__ = "comment"
    user_id = db.Column(db.Integer,db.ForeignKey("user.id")) # 用户id
    parent_id = db.Column(db.Integer) # 评论的父id
    article_id = db.Column(db.Integer,db.ForeignKey("article.id")) # 评论的文章id
    reply_comment_id = db.Column(db.Integer) # 回复的评论id
    reply_id = db.Column(db.Integer,db.ForeignKey("user.id")) # 回复的评论的用户id
    content = db.Column(db.String(320)) # 评论的内容
    created_date =db.Column(db.DateTime, default=datetime.datetime.now) # 评论时间


# 用户
class User(BaseModel):
    __tablename__ = "user"
    username = db.Column(db.String(32),unique=True)
    email = db.Column(db.String(100),unique=True)

    comment_user = db.relationship(
        "Comment",
        foreign_keys = [Comment.user_id],
        lazy='dynamic',
        backref="user_comment",
    )
    comment_reply = db.relationship(
        "Comment",
        foreign_keys=[Comment.reply_id],
        lazy='dynamic',
        backref="reply_comment",
    )



# 留言
class LeaveMessage(BaseModel):
    __tablename__ = "leave_message"
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    reply_id = db.Column(db.Integer)
    content = db.Column(db.String(320))
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)

    user = db.relationship(
        "User",
        backref='leave_message'
    )

# 音乐
class Music(BaseModel):
    title = db.Column(db.String(300))
    singer = db.Column(db.String(100))
    image = db.Column(db.String(200))
    src = db.Column(db.String(300))

