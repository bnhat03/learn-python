from .extension import ma

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'fullName', 'passwordHash', 'email', 'avatar', 'bio')

class PostSchema(ma.Schema):
    class Meta:
        fields = ('id', 'userId', 'content', 'image')

class CommentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'postId', 'userId', 'content')

class LikeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'postId', 'userId')