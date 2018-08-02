import os
import tornado.web
from utils import photo
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
        # 从settings拿到iamges的路径
        images_path = os.path.join(self.settings.get('static_path'), 'uploads')
        # 调用get_images拿到拿到图片
        images = photo.get_images(images_path)
        # 传入模板
        self.render('index.html', images=images)

class ExploreHandler(tornado.web.RequestHandler):
    """
    Explore page, photo of other users.
    """
    def get(self, *args, **kwargs):
        img_urls = photo.get_images('./static/uploads/thumbs')
        self.render('explore.html', images=img_urls)

class PostHandler(tornado.web.RequestHandler):
    """
    Single photo page, and maybe comments.
    """
    def get(self, *args, **kwargs):
        self.render('post.html', post_id=kwargs['post_id'])

class UploadHandler(tornado.web.RequestHandler):
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
            with open('./static/uploads/' + img_file['filename'], 'wb') as f:
                f.write(img_file['body'])
            photo.make_thumb('./static/uploads/'+img_file['filename'])
        self.write({'got file': img_file['filename']})

