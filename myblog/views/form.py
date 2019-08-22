from flask_wtf import FlaskForm # 用来定义表单的父类
import wtforms # 可以用来定义字段以及进行表单验证，类似django中的forms
from myblog.models import db,Admin
import hashlib

def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    f_md5 = md5.hexdigest()
    md5.update(f_md5.encode())
    return md5.hexdigest()


class LoginForm(FlaskForm):
    username = wtforms.StringField(
        label="用户名",
        widget=wtforms.widgets.TextInput(),
        validators=[
            wtforms.validators.DataRequired("用户名不可以为空！"),
            wtforms.validators.Length(8,18,message="用户名必须在8-18位之间！")
        ]
    )
    password = wtforms.PasswordField(
        label="密码",
        widget=wtforms.widgets.PasswordInput(),
        validators=[wtforms.validators.DataRequired("密码不可以为空！")]

    )

    def validate_username(self,field):
        if Admin.query.filter_by(username=field.data).first():
            password = setPassword(self.password.data)
            if password != Admin.query.filter_by(username=field.data).first().password:
                raise wtforms.ValidationError("您输入的用户名或密码错误！")
        else:
            raise wtforms.ValidationError("您输入的用户名或密码错误！")


































