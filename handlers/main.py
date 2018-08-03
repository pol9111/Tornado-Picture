import os
import tornado.web
from utils import photo
from utils.account import add_post_for, get_post_for
from pycket.session import SessionMixin


class AuthBaseHandler(tornado.web.RequestHandler, SessionMixin):
    """
    保持登入状态
    """
    def get_current_user(self):
        return self.session.get('user_info')

class IndexHandler(AuthBaseHandler):
    """
    Home page for user, photo feeds of follow.
    """
    @tornado.web.authenticated # tornado自动验证登入
    def get(self, *args, **kwargs):
        posts = get_post_for(self.current_user)
        image_urls = [p.image_url for p in posts] # p.image_url即posts.image_url
        print(image_urls)
        print(image_urls)
        print(image_urls)
        self.render('index.html', images=image_urls)

class ExploreHandler(AuthBaseHandler):
    """
    Explore page, photo of other users.
    """
    def get(self, *args, **kwargs):
        posts = get_post_for(self.current_user)
        thumb_urls = [p.thumb_url for p in posts]
        self.render('index.html', images=thumb_urls)

class PostHandler(tornado.web.RequestHandler):
    """
    Single photo page, and maybe comments.
    """
    def get(self, post_id):
        self.render('post.html', post_id=post_id)

class UploadHandler(AuthBaseHandler):
    """
    Accept images upload.
    """
    def get(self, *args, **kwargs):
        self.render('upload.html')

    def post(self, *args, **kwargs):
        # 保存上传的图片, 并压缩, 压缩图也保存
        global img_file
        img_files = self.request.files.get('newimg', None)
        for img_file in img_files:
            base_name = 'uploads/' + img_file['filename'] # 图片路径
            save_to = os.path.join(self.settings['static_path'], base_name) # 完整图片路径
            print("save to {}".format(save_to))
            with open(save_to, 'wb') as f:
                f.write(img_file['body'])
            full_path = photo.make_thumb(save_to) # 保存缩略图
            thumb_url = os.path.relpath(full_path, self.settings['static_path'])
            # 要拿到current_user此类必须继承 AuthBaseHandler即用户系统类
            add_post_for(self.current_user, base_name, thumb_url) # 把上传的图片路径保存到数据库

        self.write({'got file': img_file['filename']})
        self.redirect('/explore')

