from flask import Blueprint
from .services import (updateCommentByIdService, deleteCommentService)
comments = Blueprint("comments", __name__)

@comments.route("/<int:id>", methods=['PUT'])
def updateCommentById(id):
    return updateCommentByIdService(id)
# delete comment
@comments.route("/<int:id>", methods=['DELETE'])
def deleteComment(id):
    return deleteCommentService(id)

