from flask import Flask, render_template, request, redirect, url_for 
from flask_login import UserMixin, LoginManager, login_required
from datetime import timedelta
from .db import db
from .auth.models import User, Post
from flask_migrate import Migrate
from .auth import auth as auth_blueprint
from werkzeug.security import generate_password_hash  
import os

app = Flask(__name__)
app.secret_key = "myblog-super-secret-key"
app.permanent_session_lifetime = timedelta(minutes=5)

# login 管理
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 資料庫設定
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "..", "instance", "blog.db")
os.makedirs(os.path.dirname(db_path), exist_ok=True)  # 確保資料夾存在
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# 掛載 Blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

# 建立資料表 + 自動建立 admin 帳號（如果不存在）
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username="admin").first():
        admin = User(
            username="admin",
            email="admin@example.com"
            password=generate_password_hash("admin123"),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin 帳號已建立（admin / admin123）")

# 路由設定
@app.route("/")
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("index.html", posts=posts)

@app.route("/new", methods=["GET", "POST"])
@login_required
def new_post():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        post = Post(title=title, content=content)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("new.html")

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", post=post)

@app.route("/posts/<int:post_id>/edit", methods=["GET", "POST"])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == "POST":
        post.title = request.form["title"]
        post.content = request.form["content"]
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("edit.html", post=post)

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("index"))

# 地端執行才會啟動伺服器
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
