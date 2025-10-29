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
    """Creates a new tag in the datatbase"""
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
