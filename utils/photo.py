import glob
import os
from PIL import Image

def get_images(path):
    """
    获取目录里的图片
    """
    images = []
    for file in glob.glob(path+'/*.jpg'):
        images.append(file)
    return images

class ImageSave(object):
    """
    辅助保存用户上传的图片, 生成缩略图, 保存图片相关, URL 用来存到数据库
    """

    upload_dir = 'uploads'
    thumb_dir = 'thumbs'
    size = (200, 200)

    def __init__(self, static_path, name):
        """

        :param static_path: 图片保存到服务器文件的路径
        :param name: 用户上传的图片名字
        """
        self.static_path = static_path
        self.name = name

    @property
    def upload_url(self):
        """图片的相对路径"""
        return os.path.join(self.upload_dir, self.name)
    # /uploads/539179818c964c925055207aa3be5df5.jpg

    @property
    def upload_path(self):
        """图片的绝对路径"""
        return os.path.join(self.static_path, self.upload_url)
    # static/uploads/539179818c964c925055207aa3be5df5.jpg

    def save_upload(self, content):
        """保存图片"""
        with open(self.upload_path, 'wb') as f:
            f.write(content)
    # 保存图片写绝对路径

    @property
    def thumb_url(self):
        """缩略图的相对路径"""
        base, _ = os.path.splitext(self.name)
        thumb_name = os.path.join('{0}_{1}x{2}.jpg'.format(base, self.size[0], self.size[1]))
        return os.path.join(self.upload_dir, self.thumb_dir, thumb_name)
    # uploads/thumbs/539179818c964c925055207aa3be5df5_200x200.jpg

    def make_thumb(self):
        """生成缩略图"""
        im = Image.open(self.upload_path)
        im.thumbnail(self.size)
        im.save(os.path.join(self.static_path, self.thumb_url), 'JPEG')



