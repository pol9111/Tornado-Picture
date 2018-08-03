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
    dirname = os.path.dirname(path)
    file, ext = os.path.splitext(os.path.basename(path))
    im = Image.open(path)
    size = (200, 200)
    im.thumbnail(size)
    save_thumb_to = os.path.join(dirname, 'thumbs', '{}_{}x{}.jpg'.format(file, *size))
    im.save(save_thumb_to, 'JPEG')
    return save_thumb_to



