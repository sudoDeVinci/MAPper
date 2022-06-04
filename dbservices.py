from db import cnx, DB_NAME
from collections import namedtuple
import mysql.connector
from mysql.connector import errorcode


# Insert User Records into table
def insert_user(followed_id, id, user_at, is_private, AVI_path, created):

    cursor = cnx.cursor(named_tuple = True)

    # Insert into the account table 
    try:
        cursor.execute("""
        INSERT INTO account (id, user_at, is_private, AVI_path, created)
        VALUES (%s, %s, %s, %s, %s);
        """, [id, user_at, is_private, AVI_path, created])

        cnx.commit()

        # Insert into the follows table
        cursor.execute("""
        INSERT INTO follows (followed_id, follower_id)
        VALUES (%s, %s);
        """, [followed_id, id])

        cnx.commit()

        return 0

    except mysql.connector.Error as error:
        return error.msg


# Get user that has not been crawled yet
def get_next_poi(current_poi_id):
    
    # Get tuple of all followers of current poi.
    cursor = cnx.cursor(named_tuple = True)

    try:
        cursor.execute("""
        SELECT follower_id FROM follows
        WHERE followed_id = %s;
        """,[current_poi_id])

        prospective_poi_ids = cursor.fetchall()

        # Check if any followers have been recorded for these ids
        # The first one which hasn't been scraped will be returned.
        
        for row in prospective_poi_ids:
            
            cursor.execute("""
            SELECT * FROM follows
            WHERE followed_id = %s LIMIT 1;
            """, [row.follower_id])

            followers = cursor.fetchone()

            if followers is None:
                return row.follower_id

        return 0

    except mysql.connector.Error as error:
        return error.msg


