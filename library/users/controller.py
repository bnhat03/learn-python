from flask import Blueprint
from .services import (addUserService, getUserByUsernameService, getAllUsersService, updateUserByIdService, deleteUserService)
users = Blueprint("users", __name__)

# add a user
@users.route("/", methods=['POST'])
def addUser():
    return addUserService()

# get user by id
@users.route("/<string:username>", methods=['GET'])
def getUserByUsername(username):
    return getUserByUsernameService(username)

# # get all 
@users.route("/", methods=['GET'])
def getAllUsers():
    return getAllUsersService()

# update 
@users.route("/<int:id>", methods=['PUT'])
def updateUserById(id):
    return updateUserByIdService(id)

# delete user
@users.route("/<int:id>", methods=['DELETE'])
def deleteUser(id):
    return deleteUserService(id)

