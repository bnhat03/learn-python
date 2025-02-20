from flask import Flask
import os
from .users.controller import users  
from .posts.controller import posts  
from .comments.controller import comments  
from .likes.controller import likes 
from .auth.controller import auth 
from .extension import db, ma
from .model import User, Post, Comment, Like
from flask_cors import CORS
from flask import current_app, send_from_directory, abort

def create_db(app):
    with app.app_context():
        try:
            db.create_all()
            print("Database connected and tables created!")
        except Exception as e:
            print(f"Database error: {e}")


def create_app(config_file="config.py"):
    app = Flask(__name__)
    
    app.config.from_pyfile(config_file)

    db.init_app(app)
    ma.init_app(app)

    create_db(app)

    # Đăng ký Blueprint
    app.register_blueprint(users, url_prefix="/api/users")
    app.register_blueprint(posts, url_prefix="/api/posts")
    app.register_blueprint(comments, url_prefix="/api/comments")
    app.register_blueprint(likes, url_prefix="/api/likes")
    app.register_blueprint(auth, url_prefix="/api/auth")
    @app.route('/uploads/<path:filename>')
    def get_uploaded_file(filename):
        # Lấy cấu hình UPLOAD_FOLDER, mặc định là "../uploads" (nằm ở cấp cha của thư mục chứa app.py)
        upload_folder = current_app.config.get('UPLOAD_FOLDER', os.path.join('..', 'uploads'))
        
        # Nếu UPLOAD_FOLDER không phải là đường dẫn tuyệt đối, chuyển nó thành đường dẫn tuyệt đối dựa vào current_app.root_path
        if not os.path.isabs(upload_folder):
            upload_folder = os.path.abspath(os.path.join(current_app.root_path, upload_folder))
        
        # Tạo đường dẫn đầy đủ đến file
        file_path = os.path.join(upload_folder, filename)
        
        # Kiểm tra file có tồn tại không
        if not os.path.exists(file_path):
            current_app.logger.error(f"File not found: {file_path}")
            abort(404)
        
        return send_from_directory(upload_folder, filename)
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

    return app
