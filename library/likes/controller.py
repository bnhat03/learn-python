from flask import Blueprint
from .services import (unlikePostService, getUserLikesService)
likes = Blueprint("likes", __name__)

# unlike
@likes.route("/<int:postId>", methods=['DELETE'])
def unlikePost(postId):
    return unlikePostService(postId)

@likes.route("/user/<int:userId>", methods=['GET'])
def getUserLikes(userId):
    return getUserLikesService(userId)

