from collections import namedtuple
from db import cnx, DB_NAME


# Database schema
def init_db():
    cursor = cnx.cursor()

    cursor.execute(f"""
        CREATE DATABASE IF NOT EXISTS {DB_NAME};
    """)

    cnx.database = DB_NAME

    # Select the db
    cursor.execute(f"""
        USE {DB_NAME};
    """)

    # Table to hold account details
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS account (
            id VARCHAR(36) PRIMARY KEY ,
            user_at VARCHAR(50) NOT NULL UNIQUE,
            is_private BOOLEAN NOT NULL,
            AVI_path VARCHAR(500),
            created DATE NOT NULL
        );
    """)

    # Create the followers table
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS follows (
            followed_id VARCHAR(36) NOT NULL,
            follower_id VARCHAR(36) NOT NULL,

            FOREIGN KEY fk_followed_id(followed_id)
                REFERENCES account(id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE,
            
            FOREIGN KEY fk_follower_id(follower_id)
                REFERENCES account(id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE,
            
            CONSTRAINT pk PRIMARY KEY (followed_id, follower_id)
        );
    """)


# Check if db exists
def db_exists():
    cursor = cnx.cursor()

    cursor.execute("""
        SHOW DATABASES LIKE '{DB_NAME}';
    """)

    return bool(len(cursor.fetchall()))


# Attempt to either connect to/initialize db
def db_connect():
    if not db_exists():
        print(f"Database {DB_NAME} does not exist, Initializing . . .\n")
        init_db()
    else:
        cnx.database = DB_NAME