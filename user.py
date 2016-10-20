import flask_login


class User(flask_login.UserMixin):

    def __init__(self, username):
        self.username = username

    def get_id(self):
        return self.username

    def has_access(self, access):
        print("Checking access for %s" % self.username)
        return access == self.username
