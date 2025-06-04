from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from myblog.db import db
from datetime import datetime
import pytz  # 時區處理用

# 自訂函式：回傳台灣現在時間
def taiwan_time():
    return datetime.now(pytz.timezone("Asia/Taipei"))

# 使用者資料模型
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)  # 使用者名稱
    email = db.Column(db.String(120), nullable=False, unique=True)    # 電子郵件
    password = db.Column(db.String(200), nullable=False)              # 密碼（應加密儲存）
    is_admin = db.Column(db.Boolean, default=False)                   # 是否為管理員
    created_at = db.Column(db.DateTime, default=taiwan_time)          # 創建時間

    def __repr__(self):
        return f"<User {self.id} - {self.username}>"

# 發文模型
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=taiwan_time)

    def __repr__(self):
        return f"<Post {self.id} - {self.title}>"