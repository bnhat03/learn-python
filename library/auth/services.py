from library.extension import db
from library.model import User
from flask import request, jsonify
from sqlalchemy.sql import func
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
load_dotenv()
bcrypt = Bcrypt()

def loginService():
    data = request.json
    password = data['password']
    email = data['email']
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401

    hashed_password = user.passwordHash
    # Kiểm tra mật khẩu
    if bcrypt.check_password_hash(hashed_password, password):
        # Tạo token JWT với thông tin user_id và thời hạn 1 ngày
        token = jwt.encode(
            {
                "user_id": user.id,
                "exp": datetime.utcnow() + timedelta(days=1)
            },
            os.environ.get("SECRET_KEY"),
            algorithm="HS256"
        )
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        return jsonify({"message": "Login successful", "token": token,"userId": user.id, "username": user.username}), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401

