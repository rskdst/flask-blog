from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from myblog import app
from myblog.views.register import *

manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command("db",MigrateCommand)

# 创建后台管理者
@manager.command
def create_manager():
    create_admin()



if __name__ == "__main__":
    manager.run()