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


class Article(BaseModel):
    __tablename__ = "article"
    title = db.Column(db.String(100))
    author = db.Column(db.String(20))
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)
    update_date = db.Column(db.DateTime, nullable=False,default=datetime.datetime.now,onupdate=datetime.datetime.now)
    description = db.Column(db.String(200))
    content = db.Column(db.Text)
    article_type = db.Column(db.String(3))

    tag = db.relationship("Tag",
        secondary=Article_Tag,
        lazy='dynamic',
        backref="article",
    )
    comment = db.relationship(
        "Comment",
        lazy='dynamic',
        backref="article",
    )



class Tag(BaseModel):
    __tablename__ = "tag"
    name = db.Column(db.String(32), unique=True)


class Comment(BaseModel):
    __tablename__ = "comment"
    user_id = db.Column(db.Integer,db.ForeignKey("user.id")) # 用户id
    parent_id = db.Column(db.Integer,db.ForeignKey("user.id")) # 评论的父id
    article_id = db.Column(db.Integer,db.ForeignKey("article.id")) # 评论的文章id
    reply_id = db.Column(db.Integer,nullable=True) # 回复的评论id
    content = db.Column(db.String(320)) # 评论的内容
    created_date =db.Column(db.DateTime, default=datetime.datetime.now) # 评论时间


class User(BaseModel):
    __tablename__ = "user"
    username = db.Column(db.String(32),unique=True)
    email = db.Column(db.String(100),unique=True)

    user = db.relationship(
        "Comment",
        foreign_keys = [Comment.user_id],
        lazy='dynamic',
        backref="user_comment",
    )
    parent = db.relationship(
        "Comment",
        foreign_keys = [Comment.parent_id],
        lazy='dynamic',
        backref="parent_comment",
    )

