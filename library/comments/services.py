from library.extension import db
from library.library_ma import CommentSchema
from library.model import Comment
from flask import request, jsonify
from sqlalchemy.sql import func
comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)

def updateCommentByIdService(id):
    comment = Comment.query.get(id)
    # data = request.json
    data = request.form.to_dict()
    if comment:
        try:
            comment.content = data["content"]
            db.session.commit()
            return jsonify({"message": "Update comment infor successfully!"}), 200
        except IndentationError:
            db.session.rollback()
            return jsonify({"message": "Can not update comment!"}), 400
    else:
        return "Not found comment"

def deleteCommentService(id):
    comment = Comment.query.get(id)
    if comment:
        try:
            db.session.delete(comment)
            db.session.commit()
            return jsonify({"message": "Delete this comment successfully!"}), 200
        except IndentationError:
            db.session.rollback()
            return jsonify({"message": "Can not delete comment!"}), 400
    else:
        return "Not found comment"


