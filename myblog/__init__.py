from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
db = SQLAlchemy()
pymysql.install_as_MySQLdb()

app = Flask(__name__,template_folder="templates",static_folder="statics",static_url_path="/statics")
app.config.from_object("myblog.settings.DebugConfig")
db.init_app(app)

from .views.index import index
from .views.article import article
from .views.message import message
from .views.backstage import backstage


app.register_blueprint(index)
app.register_blueprint(article)
app.register_blueprint(message)
app.register_blueprint(backstage)



