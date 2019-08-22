from myblog.models import db,Admin
import hashlib

def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    f_md5 = md5.hexdigest()
    md5.update(f_md5.encode())
    return md5.hexdigest()


def create_admin():
    username = "1358007058"
    password = "lj950824,."
    password = setPassword(password)
    manager = Admin(username=username,password=password)
    db.session.add(manager)
    db.session.commit()
