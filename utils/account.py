import hashlib
from models.account import User, session, Post
from datetime import datetime

def hash_it(password):
    return hashlib.md5(password.encode()).hexdigest()

def authenticate(username, password):
    """
    验证用户账号信息
    """
    if username and password:
        hash_pass = User.get_pass(username)
        if hash_pass and hash_it(password) == hash_pass:
            return True
    return False

def login(username):
    """
    记录用户登入时间, 并保存的数据库的last_login
    """
    t = datetime.now()
    print("user: {} login at {}".format(username, t))
    user_query = session.query(User).filter_by(
        name=username)
    session.query(User).filter_by(name=username).update({
        User.last_login: t})
    session.commit()

def register(username, password, email):
    """
    把用户注册信息添加进数据库
    """
    if User.is_exists(username):
        return {'msg': 'username is exists'}

    hash_pass = hash_it(password)
    User.add_user(username, password=hash_pass, email=email)
    return {'msg': 'ok'}

def add_post_for(username, image_url, thumb_url):
    """
    保存特定用户的图片
    """
    user = session.query(User).filter_by(name=username).first()
    post = Post(image_url=image_url, thumb_url=thumb_url, user=user)
    session.add(post)
    session.commit()
    # return post.id

def get_post_for(username):
    """
    获取用户图片列表
    """
    user = session.query(User).filter_by(name=username).first()
    posts = session.query(Post).filter_by(user=user)
    return posts

