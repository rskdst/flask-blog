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
                          secondary = Article_Tag,
                          backref = "article",
                          lazy='subquery'
                     )


class Tag(BaseModel):
    __tablename__ = "tag"
    name = db.Column(db.String(32), unique=True)






