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

def make_thumb(path):
    """
    把传入的图片压缩成缩略图
    """
    file, ext = os.path.splitext(os.path.basename(path))
    im = Image.open(path)
    im.thumbnail((200, 200))
    im.save('./static/uploads/thumbs/{}_{}x{}.jpg'.format(file, 200, 200), "JPEG")




