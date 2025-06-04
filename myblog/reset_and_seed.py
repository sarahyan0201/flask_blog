import os
import shutil
from myblog.app import app, db
from myblog.auth.models import User, Post  # 加上 Post
from flask_migrate import upgrade, init, migrate
from werkzeug.security import generate_password_hash
from sqlalchemy import text
from datetime import datetime
import pytz  # 加上 pytz 時區套件

def taiwan_time():
    return datetime.now(pytz.timezone("Asia/Taipei"))

with app.app_context():
    db_path = os.path.join(app.instance_path, "blog.db")
    
    if os.path.exists(db_path):
        print("Deleting old database...")
        os.remove(db_path)
    
    if os.path.exists("migrations"):
        print("🧹 Removing old migrations...")
        shutil.rmtree("migrations")
    
    print("Initializing migrations...")
    init()
    migrate(message="Fresh start with is_admin")
    upgrade()

    print("👑 Creating admin user...")
    hashed_password = generate_password_hash("admin123")
    admin = User(username="admin", password=hashed_password, is_admin=True)
    db.session.add(admin)
    db.session.commit()

    print("Admin user created.")

    print("Creating a test post with Taiwan time...")
    post = Post(title="測試1", content="終於成功了!!!", created_at=taiwan_time())
    db.session.add(post)
    db.session.commit()

    print("Test post created.")

    print("User table structure:")
    result = db.session.execute(text("PRAGMA table_info(user);")).fetchall()
    for row in result:
        print(row)
