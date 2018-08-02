import tornado.web
from utils.account import authenticate
from .main import AuthBaseHandler

class LoginHandler(AuthBaseHandler):
    """
    用户登入处理
    """
    def get(self, *args, **kwargs):
        self.render('login.html')

    def post(self, *args, **kwargs):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)

        passed = authenticate(username, password)

        if passed:
            self.session.set('user_info', username)
            self.redirect('/')
        else:
            self.write({'msg': 'login fail'})

class LogoutHandler(AuthBaseHandler):
    """
    用户登出处理
    """
    def get(self, *args, **kwargs):
        self.session.set('user_info', '')
        self.redirect('/login')


class SignupHandler(AuthBaseHandler):
    def get(self, *args, **kwargs):
        self.render('signup.html')

    def psot(self):
        username = self.get_argument('username', '')
        email = self.get_argument('email', '')
        password1 = self.get_argument('password1', '')
        password2 = self.get_argument('password2', '')

        if username and password1 and password2:
            if password1 != password2:
                self.write({'msg': '两次输入的密码不匹配'})
            else:
                pass

