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
        img_files = self.request.files.get('newimg', None)
        for img in img_files:
            saver = photo.ImageSave(self.settings['static_path'], img['filename'])
            saver.save_upload(img['body'])
            saver.make_thumb()
            add_post_for(self.current_user, saver.upload_url, saver.thumb_url) # 把上传的图片路径保存到数据库
            print("save to {}".format(saver.upload_path))

        self.write({'got file': img_files[0]['filename']})
        self.redirect('/explore')

