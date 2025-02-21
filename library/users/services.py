from library.extension import db
from library.library_ma import UserSchema
from library.model import User
from flask import request, jsonify
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

user_schema = UserSchema()
users_schema = UserSchema(many=True)

def addUserService():
    data = request.form.to_dict()
    username = data['username']
    fullName = data['fullName']
    password = data['password']    
    email = data['email']
    avatar = data['avatar']
    bio = data['bio']
    try:
        # user existed
        user = User.query.filter((User.email == email) | (User.username == username)).all()
        if user: 
            return jsonify({"message": "Username or email existed!"}), 400
        else:
            passwordHash = bcrypt.generate_password_hash(password).decode('utf-8')
            newUser = User(username, fullName, passwordHash, email, avatar, bio)
            db.session.add(newUser)
            db.session.commit()
            return jsonify({"message": "Add the user success!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Can not add user!", "error": str(e)}), 400

def getUserByUsernameService(username):
    user = User.query.filter_by(username=username).first()
    if user:
        result = user_schema.dump(user) # => DICT
        result.pop("passwordHash", None)
        return jsonify(result)
    else:
        return jsonify({"message": "Not found user"}), 404
    
def getAllUsersService():
    users = User.query.all()
    if users:
        result = users_schema.dump(users)  # => DICT
        for user in result:
            user.pop("passwordHash", None)  
        return jsonify(result)
    else:
        return jsonify({"message": "Not found users!"}), 404

def updateUserByIdService(id):
    user = User.query.get(id)
    # data = request.json
    data = request.form.to_dict()
    if user:
            try:
                user.fullName = data["fullName"]
                user.avatar = data["avatar"]
                user.bio = data["bio"]
                db.session.commit()
                return jsonify({"message": "Update user infor successfully!"}), 200
            except IndentationError:
                db.session.rollback()
                return jsonify({"message": "Can not delete user!"}), 400
    else:
        return "Not found user"


def deleteUserService(id):
    user = User.query.get(id)
    if user:
        try:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": "Delete this user successfully!"}), 200
        except IndentationError:
            db.session.rollback()
            return jsonify({"message": "Can not delete user!"}), 400
    else:
        return "Not found user"

