from .extension import db

class User(db.Model):
    __tablename__ = 'user'
    # column
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    fullName = db.Column(db.String(100), nullable=False)
    passwordHash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    avatar = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    # (eager loading)
    posts = db.relationship("Post", backref="user", lazy="joined")
    comments = db.relationship("Comment", backref="user", lazy="joined")
    likes = db.relationship("Like", backref="user", lazy="joined")
    #__init__
    def __init__(self, username, fullName, passwordHash, email, avatar, bio):
        self.username = username
        self.fullName = fullName
        self.passwordHash = passwordHash
        self.email = email
        self.avatar = avatar
        self.bio = bio

class Post(db.Model):
    __tablename__ = 'post'
    # column
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.String(255))
    image = db.Column(db.String(255))
    # (eager loading)
    comments = db.relationship("Comment", backref="post", lazy="joined")
    likes = db.relationship("Like", backref="post", lazy="joined")
    #__init__
    def __init__(self, userId, content, image):
        self.userId = userId
        self.content = content
        self.image = image

class Comment(db.Model):
    __tablename__ = 'comment'
    # column
    id = db.Column(db.Integer, primary_key=True)
    postId = db.Column(db.Integer, db.ForeignKey('post.id'))
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.String(255), nullable=False)
    #__init__
    def __init__(self, postId, userId, content):
        self.postId = postId
        self.userId = userId
        self.content = content

class Like(db.Model):
    __tablename__ = 'like'
    # column
    id = db.Column(db.Integer, primary_key=True)
    postId = db.Column(db.Integer, db.ForeignKey('post.id'))
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    #__init__
    def __init__(self, postId, userId):
        self.postId = postId
        self.userId = userId
