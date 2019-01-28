from recently_played_playlists.db.db import map_playlist_params_to_query
from recently_played_playlists.db.db import get_user_id_for_username

# This is only an acceptance test as it gets a user id from MySQL.
# I should just mock this, buy mysql is setup on travis ci, and I'm being lazy.

def test_map_playlist_params_to_query_basic():
    # Use defaults from recently-played-playlists-parser, and onyl required params.
    user_id = get_user_id_for_username('test_user')

    params = {}
    params['username'] = 'test_user'
    params['time_begin'] = 0
    params['time_end'] = 99999999999
    params['agby'] = 'track_id'
    params['comparator'] = -1
    params['count'] = -1
    params['limit'] = -1

    query = map_playlist_params_to_query(params)

    assert query.strip() == """
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
        time_begin=params['time_begin'],
        time_end=params['time_end'],
        agby=params['agby'],
    ).strip()


def test_map_playlist_params_to_query_all_params():
    user_id = get_user_id_for_username('test_user')

    params = {}
    params['username'] = 'test_user'
    params['time_begin'] = 1234567890
    params['time_end'] = 1999999999
    params['agby'] = 'track_id'
    params['comparator'] = 2
    params['count'] = 30
    params['limit'] = 10

    query = map_playlist_params_to_query(params)
    assert query.strip() == """
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
     WHERE num_plays {comparator} {count} ORDER BY num_plays {order_by} LIMIT {limit}
""".format(
        user_id=user_id,
        time_begin=params['time_begin'],
        time_end=params['time_end'],
        agby=params['agby'],
        comparator='>',
        count=params['count'],
        order_by='DESC',
        limit=params['limit'],
    ).strip()
