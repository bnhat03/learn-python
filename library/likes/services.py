from library.extension import db
from library.library_ma import LikeSchema
from library.model import Like, Post, Comment
from flask import request, jsonify, g, current_app
from sqlalchemy.sql import func
import json
from sqlalchemy.orm import joinedload
from ..auth_middleware import token_required
likes_schema = LikeSchema(many=True)

@token_required
def unlikePostService(postId):
    userId = g.current_user.get("user_id")
    like = Like.query.filter(Like.postId == postId, Like.userId == userId).first()
    if like:
        try:
            db.session.delete(like)
            db.session.commit()
            return jsonify({"message": "Unlike this post successfully!"}), 200
        except IndentationError:
            db.session.rollback()
            return jsonify({"message": "Can not unlike this post!"}), 400
    else:
        return "Not found like"

def getUserLikesService(userId):
    try:
        posts = (
            Post.query
            .join(Like, Post.id == Like.postId)
            .options(
                joinedload(Post.user),
                joinedload(Post.comments).joinedload(Comment.user),
                joinedload(Post.likes)
            )
            .filter(Like.userId == userId)
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