from dbinit import cnx, DB_NAME
import mysql.connector
from mysql.connector import errorcode

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


    # Create table to hold account details
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS account (
            id VARCHAR(36) PRIMARY KEY ,
            user_at VARCHAR(50) NOT NULL UNIQUE,
            is_private BOOLEAN NOT NULL,
            AVI_path VARCHAR(500),
            description VARCHAR(165),
            created DATE NOT NULL
        );
    """)
    cnx.commit()

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
    cnx.commit()
    #-----------------------------------------------------------------#
    
    #-----------------------------------------------------------------#
    # Create the table to hold MAP scores
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS MAP_score (
            user_id VARCHAR(36) NOT NULL,
            score DECIMAL(4,3) NOT NULL,

            FOREIGN KEY fk_user_id(user_id)
                REFERENCES account(id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE,
            
            CONSTRAINT pk PRIMARY KEY (user_id, score)
        );
    """)
    cnx.commit()
    # Create the table to hold ZOO scores
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS ZOO_score (
            user_id VARCHAR(36) NOT NULL,
            score DECIMAL(4,3) NOT NULL,

            FOREIGN KEY fk_user_id(user_id)
                REFERENCES account(id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE,
            
            CONSTRAINT pk PRIMARY KEY (user_id, score)
        );
    """)

    cnx.commit()
    #-----------------------------------------------------------------#

    #-----------------------------------------------------------------#
# Check if db exists
def db_exists():
    cursor = cnx.cursor()

    cursor.execute(f"""
        SHOW DATABASES LIKE '{DB_NAME}';
    """)

    return not not len(cursor.fetchall())


# Attempt to either connect to/initialize db
def db_connect():
    try:
        if not db_exists():
            print(f"\nDatabase {DB_NAME} does not exist, Initializing . . .\n")
            init_db()
            print(f">> Connected to Database '{DB_NAME}'")
        else:
            cnx.database = DB_NAME
            print(f">> Connected to Database '{DB_NAME}'")
        

        return True
    except mysql.connector.Error as error:
        print("\nERROR: Could not connect to database instance.\n\t└", error.msg)
        return False