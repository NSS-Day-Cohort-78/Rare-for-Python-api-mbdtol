import sqlite3
import json

def get_all_tags():
    """Get all tags"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        SELECT
            t.id,
            t.label
        FROM Tags t
        """,
        )

        tags = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            tag = {
                "id": row["id"],
                "label": row["label"],
            }

            tags.append(tag)

    return json.dumps(tags)

def create_tag(tag):
    """Creates a new tag in the database"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
        """
        INSERT INTO Tags
            (label)
        VALUES
            (?)
        """,
            (
                tag["label"],
            ),
        )

        id = db_cursor.lastrowid

        tag["id"] = id

    return json.dumps(tag)

def delete_tag(tag_id):
    """Deletes a tag from the database

    Args:
        tag_id (int): The id of the tag to delete

    Returns:
        bool: True if update was successful
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            DELETE FROM Tags
            WHERE id = ?
            """,
            (tag_id,)
        )

        rows_affected = db_cursor.rowcount

        return rows_affected > 0

def update_tag(tag_id, tag_data):
    """Updates a tag in the database

    Args:
        tag_id (int): The id of the tag to update
        tag_data (dict): The updated tag data

    Returns:
        bool: True if update was successful
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            UPDATE Tags
            SET
                label = ?
            WHERE id = ?
            """,
            (
                tag_data["label"],
                tag_id,
            ),
        )

        rows_affected = db_cursor.rowcount

        return rows_affected > 0

def get_tag_by_id(tag_id):
    """Get single tag by its id

    Args:
        tag_id (int): The id of the tag

    Returns:
        json string: The selected tag
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        SELECT
            t.id,
            t.label
        FROM Tags t
        WHERE t.id = ?
        """,
            (tag_id,),
        )

        row = db_cursor.fetchone()

        tag = {
            "id": row["id"],
            "label": row["label"]
        }

    return json.dumps(tag)
