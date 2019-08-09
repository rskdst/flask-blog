class BaseConfig(object):
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DebugConfig(BaseConfig):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "Student_test.sqlite")
    SQLALCHEMY_DATABASE_URI = "mysql://root:123@localhost:9508/blog_flask"

