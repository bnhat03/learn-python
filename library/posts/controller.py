from flask import Blueprint
from .services import (
    addPostService, 
    getPostByIdService, 
    getAllPostsService, 
    updatePostByIdService, 
    deletePostService, 
    getPostsFromUserService, 
    addCommentToPostService, 
    getPostCommentsService,
    likePostService,
    getPostLikesService)
posts = Blueprint("posts", __name__)

# add a post
@posts.route("/", methods=['POST'])
def addPost():
    return addPostService()

# get post by id
@posts.route("/<int:id>", methods=['GET'])
def getPostById(id):
    return getPostByIdService(id)

# # get all post
@posts.route("/", methods=['GET'])
def getAllPosts():
    return getAllPostsService()

# update post
@posts.route("/<int:id>", methods=['PUT'])
def updatePostById(id):
    return updatePostByIdService(id)

# delete post
@posts.route("/<int:id>", methods=['DELETE'])
def deletePost(id):
    return deletePostService(id)

@posts.route("/user/<int:userId>", methods=['GET'])
def getPostsFromUser(userId):
    return getPostsFromUserService(userId)

# comment
@posts.route("/<int:postId>/comments", methods=['POST'])
def addCommentToPost(postId):
    return addCommentToPostService(postId)

@posts.route("/<int:postId>/comments", methods=['GET'])
def getPostComments(postId):
    return getPostCommentsService(postId)

# like
@posts.route("/<int:postId>/likes", methods=['POST'])
def likePost(postId):
    return likePostService(postId)

@posts.route("/<int:postId>/likes", methods=['GET'])
def getPostLikes(postId):
    return getPostLikesService(postId)
