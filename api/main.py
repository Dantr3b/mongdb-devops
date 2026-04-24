import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from pymongo import MongoClient
from bson import ObjectId

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_mysql_conn():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "db_mysql"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_ROOT_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE", "ynov-ci"),
        port=3306,
    )


def get_mongo_db():
    client = MongoClient(
        host=os.getenv("MONGO_HOST", "db_mongo"),
        port=27017,
        username=os.getenv("MONGO_INITDB_ROOT_USERNAME"),
        password=os.getenv("MONGO_INITDB_ROOT_PASSWORD"),
        authSource="admin",
    )
    return client["blog_db"]


@app.get("/users")
def get_users():
    try:
        conn = get_mysql_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM utilisateurs")
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"utilisateurs": records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/posts")
def get_posts():
    try:
        db = get_mongo_db()
        posts = list(db.posts.find({}, {"_id": 0}))
        return {"posts": posts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health():
    errors = []

    # Check MySQL
    try:
        conn = get_mysql_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM utilisateurs")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        if count < 4:
            errors.append(f"MySQL: expected 4 users, got {count}")
    except Exception as e:
        errors.append(f"MySQL error: {str(e)}")

    # Check MongoDB
    try:
        db = get_mongo_db()
        count = db.posts.count_documents({})
        if count != 5:
            errors.append(f"MongoDB: expected 5 posts, got {count}")
    except Exception as e:
        errors.append(f"MongoDB error: {str(e)}")

    if errors:
        raise HTTPException(status_code=503, detail={"status": "unhealthy", "errors": errors})

    return {"status": "OK"}
