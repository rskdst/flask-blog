from myblog import db
import datetime

class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)

class Article(BaseModel):
    __tablename__ = "article"
    title = db.Column(db.String(100))
    author = db.Column(db.String(20))
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"))
    created_date = db.Column(db.DateTime, default=datetime.datetime.now())
    update_date = db.Column(db.DateTime, default=datetime.datetime.now)
    description = db.Column(db.String(200))
    content = db.Column(db.Text)
    article_type = db.Column(db.String(3))

    tag = db.relationship("Tag", backref="article")


class Tag(BaseModel):
    __tablename__ = "tag"
    name = db.Column(db.String(32), unique=True)



