from library.extension import db
from library.library_ma import PostSchema, CommentSchema, LikeSchema
from library.model import Post, Comment, Like, User
from flask import request, jsonify, g, current_app
from werkzeug.utils import secure_filename
from sqlalchemy.sql import func
from sqlalchemy.orm import joinedload
import os
from ..auth_middleware import token_required
post_schema = PostSchema()
posts_schema = PostSchema(many=True)
comments_schema = CommentSchema(many=True)
likes_schema = LikeSchema(many=True)

@token_required
def addPostService():
    userId = g.current_user.get("user_id")
    # Lấy dữ liệu từ form
    data = request.form.to_dict()
    content = data.get("content")
    # Kiểm tra file image từ request.files
    image_path = None
    if "image" in request.files:
        image_file = request.files["image"]
        if image_file.filename != "":
            filename = secure_filename(image_file.filename) 
            # Lấy thư mục upload từ config, nếu chưa có thì tạo mới
            upload_folder = current_app.config.get("UPLOAD_FOLDER", "uploads")
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            # Tạo đường dẫn lưu file
            full_path = os.path.join(upload_folder, filename)
            image_file.save(full_path)
            # Lưu đường dẫn tương đối (để client có thể truy cập)
            image_path = f"/uploads/{filename}"
    
    try:
        # Tạo bài post mới với userId từ token, content và đường dẫn hình ảnh
        newPost = Post(userId, content, image = image_path)
        db.session.add(newPost)
        db.session.commit()
        return jsonify({"message": "Add the post success!", "image_path": image_path}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Can not add post!", "error": str(e)}), 400

def getPostByIdService(post_id):
    try:
        # Sử dụng eager loading để join user, comments (với user) và likes
        post = (
            Post.query.options(
                joinedload(Post.user),
                joinedload(Post.comments).joinedload(Comment.user),
                joinedload(Post.likes)
            )
            .filter(Post.id == post_id)
            .first()
        )
        
        if not post:
            return jsonify({"message": "Not found post"}), 404
        result = {
            "id": post.id,
            "content": post.content,
            "image": post.image,
            "user": {
                "id": post.user.id,
                "username": post.user.username,
                "fullName": post.user.fullName,
                "avatar": post.user.avatar,
                "bio": post.user.bio
            },
            "comments": [
                {
                    "id": comment.id,
                    "content": comment.content,
                    "user": {
                        "id": comment.user.id,
                        "username": comment.user.username,
                        "fullName": comment.user.fullName,
                        "avatar": comment.user.avatar,
                        "bio": comment.user.bio
                    }
                }
                for comment in post.comments
            ],
            "likes": [
                {
                    "id": like.id,
                    "userId": like.userId 
                }
                for like in post.likes
            ]
        }
        return jsonify({"data": result, "message": "Get post successfully!"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e), "message": "Error retrieving post"}), 500
    
def getAllPostsService():
    try:
        # Sử dụng eager loading để join các bảng liên quan
        posts = (
            Post.query.options(
                joinedload(Post.user),
                joinedload(Post.comments).joinedload(Comment.user),
                joinedload(Post.likes)
            )
            .all()
        )

        result = []
        for post in posts:
            post_data = {
                "id": post.id,
                "content": post.content,
                "image": post.image,
                "user": {
                    "id": post.user.id,
                    "username": post.user.username,
                    "fullName": post.user.fullName,
                    "avatar": post.user.avatar,
                    "bio": post.user.bio
                },
                "comments": [
                    {
                        "id": comment.id,
                        "content": comment.content,
                        "user": {
                            "id": comment.user.id,
                            "username": comment.user.username,
                            "fullName": comment.user.fullName,
                            "avatar": comment.user.avatar,
                            "bio": comment.user.bio
                        }
                    }
                    for comment in post.comments
                ],
                "likes": [
                    {
                        "id": like.id,
                        "userId": like.userId  
                    }
                    for like in post.likes
                ]
            }
            result.append(post_data)
        return jsonify({"data": result, "message": "Get all posts successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e), "message": "Error retrieving posts"}), 500

def updatePostByIdService(id):
    post = Post.query.get(id)
    data = request.form.to_dict()
    if post:
            try:
                post.content = data["content"]
                post.image = data["image"]
                db.session.commit()
                return jsonify({"message": "Update post infor successfully!"}), 200
            except IndentationError:
                db.session.rollback()
                return jsonify({"message": "Can not delete post!"}), 400
    else:
        return "Not found post"


def deletePostService(id):
    post = Post.query.get(id)
    if post:
        try:
            db.session.delete(post)
            db.session.commit()
            return jsonify({"message": "Delete this post successfully!"}), 200
        except IndentationError:
            db.session.rollback()
            return jsonify({"message": "Can not delete post!"}), 400
    else:
        return "Not found post"

def getPostsFromUserService(userId):
    try:
        # Sử dụng eager loading để join các bảng liên quan
        posts = (
            Post.query.options(
                joinedload(Post.user),
                joinedload(Post.comments).joinedload(Comment.user),
                joinedload(Post.likes)
            )
            .filter(Post.userId == userId)
            .all()
        )

        result = []
        for post in posts:
            post_data = {
                "id": post.id,
                "content": post.content,
                "image": post.image,
                "user": {
                    "id": post.user.id,
                    "username": post.user.username,
                    "fullName": post.user.fullName,
                    "avatar": post.user.avatar,
                    "bio": post.user.bio
                },
                "comments": [
                    {
                        "id": comment.id,
                        "content": comment.content,
                        "user": {
                            "id": comment.user.id,
                            "username": comment.user.username,
                            "fullName": comment.user.fullName,
                            "avatar": comment.user.avatar,
                            "bio": comment.user.bio
                        }
                    }
                    for comment in post.comments
                ],
                "likes": [
                    {
                        "id": like.id,
                        "userId": like.userId  
                    }
                    for like in post.likes
                ]
            }
            result.append(post_data)
        return jsonify({"data": result, "message": "Get all posts successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e), "message": "Error retrieving posts"}), 500

# comment
@token_required
def addCommentToPostService(postId):
    data = request.json
    userId = g.current_user.get("user_id")
    content = data['content']
    try:
        newComment = Comment(postId, userId, content)
        db.session.add(newComment)
        db.session.commit()
        return jsonify({"message": "Add the comment to post successfully!"}), 201
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Can not add comment to post!"}), 400
    
def getPostCommentsService(postId):
    try:
        comments = Comment.query.filter_by(postId=postId).all()  
        if comments:
            return jsonify({
                'data': comments_schema.dump(comments), 
                "message": "Get list comments from this post successfully!"
            }), 200
        
        return jsonify({
            'data': [],
            "message": "No comments available!"
        }), 200

    except Exception as e:  
        db.session.rollback()
        return jsonify({"error": str(e), "message": "Can not get comments!"}), 500

@token_required
def likePostService(postId):
    data = request.form.to_dict()
    userId = g.current_user.get("user_id")
    try:
        newLike = Like(postId, userId)
        db.session.add(newLike)
        db.session.commit()
        return jsonify({"message": "Like this post successfully!"}), 201
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Can not like post!"}), 400
    
def getPostLikesService(postId):
    try:
        likes = Like.query.filter_by(postId=postId).all()  
        
        if likes:
            return jsonify({
                'data': likes_schema.dump(likes), 
                "message": "Get list likes from this post successfully!"
            }), 200
        
        return jsonify({
            'data': [],
            "message": "No likes available!"
        }), 200
    except Exception as e:  
        db.session.rollback()
        return jsonify({"error": str(e), "message": "Can not get likes!"}), 500

    

