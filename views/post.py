import sqlite3
import json


def get_post_by_id(post_id):
    """Get single post by its id

    Args:
        post_id (int): The id of the post

    Returns:
        json string: The selected post
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
            p.approved
        FROM Posts p
        WHERE p.id = ?
        """,
            (post_id,),
        )

        row = db_cursor.fetchone()

        post = {
            "id": row["id"],
            "user_id": row["user_id"],
            "category_id": row["category_id"],
            "title": row["title"],
            "publication_date": row["publication_date"],
            "image_url": row["image_url"],
            "content": row["content"],
            "approved": row["approved"],
        }

    return json.dumps(post)


def get_categories():
    """Get all categories

    Args:
        N/A

    Returns:
        json string: A list of the categories
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        SELECT
            c.id,
                c.label
        FROM Categories c
        """
        )

        categories = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            category = {
                "id": row["id"],
                "label": row["label"],
            }

            categories.append(category)

    return json.dumps(categories)


def update_post(post_id, post_data):
    """Updates a post in the database

    Args:
        post_id (int): The id of the post to update
        post_data (dict): The updated post data

    Returns:
        bool: True if update was successful
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            UPDATE Posts
            SET
                title = ?,
                content = ?,
                category_id = ?,
                image_url = ?
            WHERE id = ?
            """,
            (
                post_data["title"],
                post_data["content"],
                post_data["category_id"],
                post_data["image_url"],
                post_id,
            ),
        )

        rows_affected = db_cursor.rowcount

        return rows_affected > 0


def create_post(post_data):
    """Creates a new post in the database"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            INSERT INTO Posts
                (user_id, category_id, title, publication_date, image_url, content, approved)
            VALUES
                (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                post_data["user_id"],
                post_data["category_id"],
                post_data["title"],
                post_data["publication_date"],
                post_data["image_url"],
                post_data["content"],
                post_data["approved"],
            ),
        )

        post_id = db_cursor.lastrowid
        post_data["id"] = post_id

        for tag_id in post_data["tags"]:
            db_cursor.execute(
                """
                INSERT INTO PostTags
                    (post_id, tag_id)
                VALUES
                    (?, ?)
                """,
                (post_id, tag_id),
            )

    return json.dumps(post_data)
