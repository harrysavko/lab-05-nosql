
#!/usr/bin/env python3
"""Generate a bookstore inventory report using MongoDB Atlas."""

import logging
import os

from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Read MongoDB credentials from environment variables
MONGODB_ATLAS_URL = os.getenv("MONGODB_ATLAS_URL")
MONGODB_ATLAS_USER = os.getenv("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PWD = os.getenv("MONGODB_ATLAS_PWD")


def main():
    """Connect to MongoDB and display books for selected authors."""

    # Check that the required environment variables exist
    if not all([
        MONGODB_ATLAS_URL,
        MONGODB_ATLAS_USER,
        MONGODB_ATLAS_PWD
    ]):
        logging.error("Missing MongoDB environment variables.")
        return

    client = None

    try:
        # Connect to MongoDB Atlas
        client = MongoClient(
            MONGODB_ATLAS_URL,
            username=MONGODB_ATLAS_USER,
            password=MONGODB_ATLAS_PWD
        )

        client.admin.command("ping")
        logging.info("Successfully connected to MongoDB Atlas.")

        # Select the database and collections
        database = client["bookstore"]
        authors = database["authors"]
        books = database["books"]

        # Include original authors and one newly added author
        author_ids = ["author_002", "author_003", "author_004"]

        # Count the selected authors
        total_authors = authors.count_documents({
            "_id": {"$in": author_ids}
        })

        print(f"\nAuthors: {total_authors}")

        # Find each author and their books
        for author_id in author_ids:
            author = authors.find_one({"_id": author_id})

            if author is None:
                logging.warning("Author %s not found.", author_id)
                continue

            print(f"\n{author['name']}")

            # Find books that reference this author's ID
            author_books = books.find({
                "author_ids": author["_id"]
            })

            for book in author_books:
                print(
                    f"  {book['title']} ({book['published_year']})"
                )

    except PyMongoError as error:
        logging.error("MongoDB error: %s", error)

    finally:
        # Always close the database connection
        if client is not None:
            client.close()
            logging.info("MongoDB connection closed.")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s"
    )
    main()
