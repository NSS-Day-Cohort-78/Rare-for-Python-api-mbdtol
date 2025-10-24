import sqlite3
import json
from datetime import datetime


def login_user(user):
    """Checks for the user in the database

    Args:
        user (dict): Contains the username and password of the user trying to login

    Returns:
        json string: If the user was found will return valid boolean of True and the user's id as the token
                     If the user was not found will return valid boolean False
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            select id, username
            from Users
            where username = ?
            and password = ?
        """,
            (user["username"], user["password"]),
        )

        user_from_db = db_cursor.fetchone()

        if user_from_db is not None:
            response = {"valid": True, "token": user_from_db["id"]}
        else:
            response = {"valid": False}

        return json.dumps(response)


def create_user(user):
    """Adds a user to the database when they register

    Args:
        user (dictionary): The dictionary passed to the register post request

    Returns:
        json string: Contains the token of the newly created user
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        Insert into Users (first_name, last_name, username, email, password, bio, created_on, active) values (?, ?, ?, ?, ?, ?, ?, 1)
        """,
            (
                user["first_name"],
                user["last_name"],
                user["username"],
                user["email"],
                user["password"],
                user["bio"],
                datetime.now(),
            ),
        )

        id = db_cursor.lastrowid

        return json.dumps({"token": id, "valid": True})


def get_posts_by_user(user_id):
    """Get all posts by a specific user

    Args:
        user_id (int): The id of the user

    Returns:
        json string: A list of posts made by the user
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved,
            u.first_name,
            u.last_name,
            c.label
        FROM Posts p
        JOIN Users u 
            ON p.user_id = u.id
        JOIN Categories c
            ON p.category_id = c.id
        WHERE p.user_id = ?
        """,
            (user_id,),
        )

        posts = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            post = {
                "id": row["id"],
                "user_id": row["user_id"],
                "author": row["first_name"] + " " + row["last_name"],
                "category_id": row["category_id"],
                "category": row["label"],
                "title": row["title"],
                "publication_date": row["publication_date"],
                "image_url": row["image_url"],
                "content": row["content"],
                "approved": row["approved"],
            }

            posts.append(post)

    return json.dumps(posts)


def get_all_posts():
    """get all posts"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved,
            u.first_name,
            u.last_name,
            c.label
        FROM Posts p
        JOIN Users u 
            ON p.user_id = u.id
        JOIN Categories c
            ON p.category_id = c.id
        """,
        )

        posts = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            post = {
                "id": row["id"],
                "user_id": row["user_id"],
                "author": row["first_name"] + " " + row["last_name"],
                "category_id": row["category_id"],
                "category": row["label"],
                "title": row["title"],
                "publication_date": row["publication_date"],
                "image_url": row["image_url"],
                "content": row["content"],
                "approved": row["approved"],
            }

            posts.append(post)

    return json.dumps(posts)


def get_user_by_id(user_id):
    """Get single user by their id

    Args:
        user_id (int): The id of the user

    Returns:
        json string: The selected user
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        SELECT
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.profile_image_url,
            (SELECT COUNT(*) FROM Posts WHERE user_id = u.id) as post_count
        FROM Users u
        WHERE u.id = ?
        """,
            (user_id,),
        )

        row = db_cursor.fetchone()

        if row is None:
            return None

        user = {
            "id": row["id"],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "email": row["email"],
            "bio": row["bio"],
            "username": row["username"],
            "profile_image_url": row["profile_image_url"],
            "post_count": row["post_count"],
        }

    return json.dumps(user)
