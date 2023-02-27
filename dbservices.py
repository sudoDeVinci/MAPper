from dbinit import cnx, DB_NAME
import mysql.connector
from mysql.connector import errorcode
from pandas import DataFrame



# Insert User Records into table
def insert_user(followed_id, id, user_at, is_private, AVI_path, description, created):

    cursor = cnx.cursor(named_tuple = True, buffered = True)

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


# Get the COUNT of the followers of a user by id. 
def indexed_followers(poi_id):
    cursor = cnx.cursor(buffered = True)

    # Select the db
    cursor.execute(f"""
        USE {DB_NAME};
    """)

    cnx.commit()

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


# Get a user's map score by id
def get_map_score(poi_id):
    cursor = cnx.cursor(buffered = True)

    # Get the count of all followers of the poi
    try:
        cursor.execute("""
        SELECT score FROM MAP_score
        WHERE user_id = %s;
        """, [poi_id])

        score = cursor.fetchone()

        # return number of records
        return score[0]
    
    except mysql.connector.Error as error:
        return error.msg

# Assign a user map score by id
def assign_map_score(poi_id, score):
    cursor = cnx.cursor(buffered = True)

    # Insert into the MAP_score table 
    try:
        cursor.execute("""
        INSERT INTO MAP_score (user_id, score)
        VALUES (%s, %s);
        """, [poi_id, score])

        cnx.commit()

    except mysql.connector.Error as error:
        return error.msg


# Get a user's zoo score by id
def get_zoo_score(poi_id):
    cursor = cnx.cursor(buffered = True)

    # Get the count of all followers of the poi
    try:
        cursor.execute("""
        SELECT score FROM ZOO_score
        WHERE user_id = %s;
        """, [poi_id])

        score = cursor.fetchone()

        # return number of records
        return score[0]

    except mysql.connector.Error as error:
        return error.msg

# Assign a user's zoo score by id 
def assign_zoo_score(poi_id, score):
    cursor = cnx.cursor(buffered = True)

    # Insert into the MAP_score table 
    try:
        cursor.execute("""
        INSERT INTO ZOO_score (user_id, score)
        VALUES (%s, %s);
        """, [poi_id, score])

        cnx.commit()

    except mysql.connector.Error as error:
        return error.msg


# Get a dataframe of all user-follower relationships
def get_follower_relationships(num: int) -> DataFrame|str:
    # Get tuple of all follower relationships over score threshold.
    cursor = cnx.cursor(named_tuple = True, buffered = True)
    try:
        """
        The following query has been limited to only return a user defined number of accounts
        As processing all accounts every time takes far too long and graphs become less readable.
        """
        cursor.execute("""
            SELECT acc1.user_at as followed_handle, acc2.user_at as follower_handle, f.followed_id, f.follower_id, m.score AS map, z.score as zoo
            FROM follows f
            JOIN account acc1
            ON acc1.id = f.followed_id
            JOIN account acc2
            ON acc2.id = f.follower_id
            JOIN map_score m
            ON f.followed_id = m.user_id
            JOIN zoo_score z
            ON z.user_id = f.followed_id
            ORDER BY RAND() LIMIT %s;
        """, [num]) 

        return DataFrame(cursor.fetchall(), columns = ['followed_handle', 'follower_handle', 'followed_id', 'follower_id', 'map', 'zoo'])

    except mysql.connector.Error as error:
        return error.ms


# Get followers of current person of interest
# Get user that has not been crawled yet
def get_next_poi(current_poi, api):

    # Get tuple of all followers of current poi.
    cursor = cnx.cursor(named_tuple = True, buffered = True)

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

            try:
                cursor.execute("""
                SELECT * FROM follows
                WHERE followed_id = %s LIMIT 1;
                """, [row.follower_id])

                followers = cursor.fetchone()

                if followers is None:
                    # We split these into two lines rather than one compound statement
                    # to minimize the number of API and  fcuntion calls.  While the difference is minimal for small
                    # networks, it compounds as the network grows.
                    p_poi = api.get_user(user_id = row.follower_id)
                    #print('Acc:', prospective_poi.name, ' | Protected: ', prospective_poi.protected)
                    if not p_poi.protected:
                        # We only want to scrape accounts which have some definitive symbol
                        m, z = calc_map_score(p_poi.name, p_poi.screen_name, p_poi.description)
                        if m >= 0.50 or z >= 0.50:
                            return row.follower_id, m, z
            except mysql.connector.Error as error:
                return error.ms

        return 0

    except mysql.connector.Error as error:
        return error.ms


# Here we calculate the map and zoo scores of an account
# Any Symbol-Score dictionaries could be implemented and tweaked here
def calc_map_score(name, user_at, description, prev_map_score = 0, prev_zoo_score = 0):

    # Description is sometimes empty so we convert to empty string
    # if description is returned as None 
    description = " " or description


    zoo_symbols = {"ζ":0.50, "zoo":0.20, "ζoo":0.60, "ς":0.35, "feral":0.15, "💄":0.35, "therian":0.15, "pro-contact":0.35, "pro-c":0.25}
    map_symbols = {"map":0.25, "nomap":0.25, "no-map":0.30, "aam":0.05, "paraphil":0.20, "ς":0.45, "pro-c":0.20, "pro-ς":0.50, "pro-contact":0.30, "anti-c":0.15, "loli":0.10,"cunny":0.025}


    # Zoo score calculation
    zoo_score = 0.25 * float(prev_zoo_score)

    for symbol in zoo_symbols.keys():
        if (symbol in name.lower()) or (symbol in description.lower()) or (symbol in user_at.lower()):
            zoo_score += zoo_symbols[symbol]
            if zoo_score >= 1.000:
                zoo_score = 1
                break

    
    # MAP score calculation
    map_score = 0.25 * float(prev_map_score)

    for symbol in map_symbols.keys():
        if (symbol in name.lower()) or (symbol in description.lower()) or (symbol in user_at.lower()):
            map_score += map_symbols[symbol]
            if map_score >= 1.00:
                map_score = 1
                break


    return (map_score, zoo_score)







