import os
import sys

from dotenv import load_dotenv
import MySQLdb

def get_db_creds():
    # Ensure secrets are loaded
    load_dotenv()
    print('printing secrets:')
    print(os.getenv('DB_HOST'))

    creds = {}
    creds['DB_HOST'] = 'localhost'
    creds['DB_USER'] = 'root'
    creds['DB_PASS'] = ''
    creds['DB_NAME'] = 'playlists'

    return creds

def conn():
    creds = get_db_creds()
    return MySQLdb.connect(
        host=creds['DB_HOST'],
        user=creds['DB_USER'],
        passwd=creds['DB_PASS'],
        db=creds['DB_NAME']
    )

def get_time_of_last_track_play(username):
    col_name = 'spotify_time_of_last_track_played'

    con = conn()
    cur = MySQLdb.cursors.DictCursor(con)
    query = f'SELECT {col_name} from users where username="{username}"'
    cur.execute(query)
    result = cur.fetchone()
    con.close()

    if not result:
        print('finding time of last track play, did not find user in db, exiting')
        sys.exit(1)
    else:
        return result[col_name]

def update_time_of_last_track_play(username, seconds_since_epoch):
    col_name = 'spotify_time_of_last_track_played'
    query = f'UPDATE users SET {col_name}="{seconds_since_epoch}" where username="{username}"'

    con = conn()
    cur = MySQLdb.cursors.DictCursor(con)
    cur.execute(query)
    con.commit()
    con.close()

def save_track_if_not_exists(track):
    '''
    track - dict, keys: name, uri, id, duration_ms
    '''
    query = f'''
        INSERT IGNORE INTO tracks 
            (name, spotify_uri, spotify_id, duration_ms)
        VALUES
            (%s, %s, %s, %s)
    '''

    values = (track['name'], track['uri'], track['id'], track['duration_ms'])
    con = conn()
    cur = MySQLdb.cursors.DictCursor(con)
    cur.execute(query, values)
    con.commit()
    con.close()

def get_all_users():
    query = f'''
    SELECT username from users
    '''

    con = conn()
    cur = MySQLdb.cursors.DictCursor(con)
    cur.execute(query)
    results = cur.fetchall()
    con.close()

    return_value = []
    for x in results:
        return_value.append(x['username'])

    return return_value

def save_played_song(username, track_uri, played_at):
    ''' Save played track into songs_played table
    Convert track_uri to the pk auto inc track_id from mysql
    '''
    user_id = get_user_id_for_username(username)
    track_id = get_track_id_for_track_uri(track_uri)

    query = f'''
        INSERT INTO songs_played
            (track_id, user_id, played_at)
        VALUES
                (%s, %s, %s)
    '''

    values = (track_id, user_id, played_at)
    con = conn()
    cur = MySQLdb.cursors.DictCursor(con)
    cur.execute(query, values)
    con.commit()
    con.close()

def get_track_id_for_track_uri(track_uri):
    col_name = 'id'
    query = f'SELECT {col_name} from tracks where spotify_uri ="{track_uri}"'

    con = conn()
    cur = MySQLdb.cursors.DictCursor(con)
    cur.execute(query)
    result = cur.fetchone()
    con.close()

    if not result:
        print(f'did not find track by track_uri {track_uri} in db, exiting')
        sys.exit(1)
    else:
        return result[col_name]

def get_user_id_for_username(username):
    col_name = 'id'
    query = f'SELECT {col_name} from users where username="{username}"'

    con = conn()
    cur = MySQLdb.cursors.DictCursor(con)
    cur.execute(query)
    result = cur.fetchone()
    con.close()

    if not result:
        print('did not find user in db, exiting')
        sys.exit(1)
    else:
        return result[col_name]

# TODO: use release_start, release_end
def filter_to_playlist(filter_args):
    '''
    '''
    user_id = get_user_id_for_username(filter_args['username'])

    # TODO avoid sql injection here. formatting params via execute only
    # works for values in WHERE clause according to the docs
    query = """
    SELECT spotify_id FROM 
        (
            SELECT 
                COUNT(*) as num_plays, 
                track_id as id 
            FROM songs_played 
                WHERE 
                    user_id={user_id}
                    AND played_at > {time_begin}
                    AND played_at < {time_end}
                GROUP BY {agby}
        ) t1 
        INNER JOIN tracks using (id)
    """.format(
        user_id=user_id,
        time_begin=filter_args['time_begin'],
        time_end=filter_args['time_end'],
        agby=filter_args['agby'],
    )

    # If comparator and count are set, add them to the query.
    if filter_args['comparator'] > -1 and filter_args['count'] > -1:
        order_by = get_order_by(filter_args['comparator'])
        comparator = get_str_of_comparator(filter_args['comparator'])
        query += ' WHERE num_plays {comparator} {count} ORDER BY num_plays {order_by}'.format(comparator=comparator, count=filter_args['count'], order_by=order_by)
    if filter_args['limit'] > -1:
        query += ' LIMIT {limit}'.format(limit=filter_args['limit'])

    print(query)
        
    con = conn()
    cur = MySQLdb.cursors.DictCursor(con)
    cur.execute(query)
    results = cur.fetchall()
    con.close()

    return_value = []
    for x in results:
        return_value.append(x['spotify_id'])

    return return_value
    

def get_order_by(comparator):
    '''
    Set the ORDER BY value for the query so that it makes sense
    with the comparator in combination with a LIMIT clause.
    comparator values:
        0: <
        1: <=
        2: >
        3: >=

    Example:
        100 tracks with >= 10 plays, we want to order by DESC and LIMIT 100
    '''
    if comparator == 0 or comparator == 1:
        return 'ASC'
    elif comparator == 2 or comparator == 3:
        return 'DESC'
    else:
        raise Exception('Bad value for comparator')

def get_str_of_comparator(comparator):
    if comparator == 0:
        return "<"
    elif comparator == 1:
        return "<="
    elif comparator == 2:
        return ">"
    elif comparator == 3:
        return ">="
    else:
        raise Exception('Bad value for comparator')
