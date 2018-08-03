import tornado.ioloop
import tornado.web
import tornado.options
from tornado.options import define, options
from handlers import main
from handlers import auth

define('port', default='8002', help='Listening port', type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            ('/', main.IndexHandler), # 主页
            ('/explore', main.ExploreHandler), # 图片探索界面, 显示缩略图
            ('/post/(?P<post_id>[0-9]+)', main.PostHandler),
            ('/upload', main.UploadHandler), # 上传图片界面
            ('/login', auth.LoginHandler), # 用户登入界面
            ('/logout', auth.LogoutHandler), # 用户登出界面
            ('/signup', auth.SignupHandler), # 用户注册界面
        ]
        settings = dict(
            debug=True,
            template_path='templates',
            static_path='static',
            login_url='/login',
            cookie_secret='tys2cv1t4h4fsdfsd5f48bvc1btb4',
            pycket={
                'engine': 'redis',
                'storage': {
                    'host': '192.168.1.8',
                    'port': 6379,
                    # 'password': '',
                    'db_sessions': 5,  #redis db index
                    'db_notifications': 11,
                    'max_connections': 2 ** 30,
                },
                'cookies': {
                    'expires_days': 30,
                },
            }
        )

        super(Application, self).__init__(handlers, **settings)

application = Application()

if __name__ == '__main__':
    tornado.options.parse_command_line()
    application.listen(options.port)
    print("Server start on port {}".format(str(options.port)))
    tornado.ioloop.IOLoop.current().start()













