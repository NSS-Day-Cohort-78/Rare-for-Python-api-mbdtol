import sqlite3
import json


def get_post_by_id(post_id):
    """Get single post by its id with all its tags

    Args:
        post_id (int): The id of the post

    Returns:
        json string: The selected post with tags array
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
            t.id as tag_id,
            t.label as tag_label
        FROM Posts p
        JOIN Users u ON p.user_id = u.id
        LEFT JOIN PostTags pt ON p.id = pt.post_id
        LEFT JOIN Tags t ON pt.tag_id = t.id
        WHERE p.id = ?
        """,
            (post_id,),
        )

        rows = db_cursor.fetchall()
        
        # Build the post object from the first row
        post = {
            "id": rows[0]["id"],
            "user_id": rows[0]["user_id"],
            "category_id": rows[0]["category_id"],
            "title": rows[0]["title"],
            "publication_date": rows[0]["publication_date"],
            "image_url": rows[0]["image_url"],
            "content": rows[0]["content"],
            "approved": rows[0]["approved"],
            "author_firstname": rows[0]["first_name"],
            "author_lastname": rows[0]["last_name"],
            "tags": []  # Start with empty tags array
        }
        
        # Collect all tags from the rows
        for row in rows:
            if row["tag_id"] is not None:  # Only add if tag exists
                tag = {
                    "id": row["tag_id"],
                    "label": row["tag_label"]
                }
                post["tags"].append(tag)

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
        conn.row_factory = sqlite3.Row
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

def delete_post(post_id):
    """Deletes a post from the database

    Args:
        post_id (int): The id of the post to delete

    Returns:
        bool: True if update was successful
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            DELETE FROM Posts
            WHERE id = ?
            """,
            (post_id,)
        )

        rows_affected = db_cursor.rowcount

        return rows_affected > 0
