from functools import wraps
from flask import request, jsonify, g
import jwt
import os
from dotenv import load_dotenv
load_dotenv()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Lấy token từ header Authorization
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"message": "Token is missing!"}), 401
        token = auth_header.split(" ")[1]
        try:
            # decode token sử dụng SECRET_KEY 
            payload = jwt.decode(token, os.environ.get("SECRET_KEY"), algorithms=["HS256"])
            # Lưu thông tin token  vào biến toàn cục g
            g.current_user = payload
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401
        return f(*args, **kwargs)
    return decorated
