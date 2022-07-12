from dbinit import cnx
import mysql.connector
from mysql.connector import errorcode


# Insert User Records into table
def insert_user(followed_id, id, user_at, is_private, AVI_path, description, created):

    cursor = cnx.cursor(named_tuple = True)

    # Insert into the account table 
    try:
        cursor.execute("""
        INSERT INTO account (id, user_at, is_private, AVI_path, description, created)
        VALUES (%s, %s, %s, %s, %s, %s);
        """, [id, user_at, is_private, AVI_path, description, created])

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


def indexed_followers(poi_id):
    cursor = cnx.cursor(named_tuple = True)

    # Get the count of all followers of the poi
    try:
        cursor.execute("""
        SELECT COUNT(*) FROM follows
        WHERE followed_id = %s;
        """, [poi_id])

        followers = cursor.fetchone()

        # return number of records
        return followers[0]
    
    except mysql.connector.Error as error:
        return error.msg


def assign_map_score(poi_id, score):
    cursor = cnx.cursor(named_tuple = True)

    # Insert into the MAP_score table 
    try:
        cursor.execute("""
        INSERT INTO MAP_score (user_id, score)
        VALUES (%s, %s);
        """, [poi_id, score])

        cnx.commit()

    except mysql.connector.Error as error:
        return error.msg


def assign_zoo_score(poi_id, score):
    cursor = cnx.cursor(named_tuple = True)

    # Insert into the MAP_score table 
    try:
        cursor.execute("""
        INSERT INTO ZOO_score (user_id, score)
        VALUES (%s, %s);
        """, [poi_id, score])

        cnx.commit()

    except mysql.connector.Error as error:
        return error.msg


# Get followers of current person of interest
# Get user that has not been crawled yet
def get_next_poi(current_poi):

    # Get tuple of all followers of current poi.
    cursor = cnx.cursor(named_tuple = True)

    current_poi_id = current_poi.id_str

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
        return error.ms

def calc_map_score(new_poi, prev_map_score, prev_zoo_score):
    zoo_symbols = ["ζ","zoo", "ζoo","ς","feral","💄","therian"]
    map_symbols = ["map","nomap","aam","paraphile","ς"]

    # Zoo score calculation
    base = 0.4 * prev_zoo_score
    zoo_self = 0
    for symbol in zoo_symbols:
        if (symbol in new_poi.username) or (symbol in new_poi.description) or (symbol in new_poi.name):
            zoo_self = 0.6
            break
    zoo_score = zoo_self + base
    
    # MAP score calculation
    base = 0.4 * prev_zoo_score
    map_self = 0
    for symbol in map_symbols:
        if (symbol in new_poi.username) or (symbol in new_poi.description) or (symbol in new_poi.name):
            map_self = 0.6
            break
    map_score = map_self + base

    return (map_score, zoo_score)







