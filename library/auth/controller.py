from flask import Blueprint
from .services import (loginService)
auth = Blueprint("auth", __name__)

@auth.route("/login", methods=['POST'])
def login():
    return loginService()

#note: Chưa làm
# @auth.route("/sign-up", methods=['POST'])
# def signup():
#     return signupService()


