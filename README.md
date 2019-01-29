[![Build Status](https://travis-ci.org/ndelnano/recently-played-playlists.svg?branch=master)](https://travis-ci.org/ndelnano/recently-played-playlists)

# About
This repo holds various functionalities for supporting the [recently-played-playlists-parser](https://github.com/ndelnano/recently-played-playlists-parser).
- Utilites for saving data of a user's recently played tracks from the spotify API and inserting them into MySQL
  - Poll spotify's [get-recently-played endpoint](https://developer.spotify.com/documentation/web-api/reference/player/get-recently-played/) and save this data to MySQL. I poll this API endpoint as a cron to preserve my listening history.
  - Save various song data not included in the get-recently-played endpoint by calling the [get-several-tracks endpoint](https://developer.spotify.com/documentation/web-api/reference/tracks/get-several-tracks/) Currently, this is in development for adding the `release_date` attribute to each track.
- HTTP API for supporting queries from playlist-parser
  - /process_filter -- Transform a `Playlist` (list of filters) into an SQL query, execute it, and return a list of spotify `track_id`'s.
  - /make_playlist -- Create a playlist, given a list of spotify `track_id`'s.

You should not care to interact with these endpoints youself -- you should interact with them via the recently-played-playlists-parser.

# Installing and running
See [recently-played-playlists-puppet](https://github.com/ndelnano/recently-played-playlists-puppet) for a puppet module and detailed instructions.

## Environment variables
Leaving these here serves more as documentation. If you are installing, you really want to look at the puppet repo.
- SPOTIFY_CLIENT_ID
- SPOTIFY_CLIENT_SECRET
- DB_HOST
- DB_USER
- DB_PASS
- DB_NAME
- FLASK_APP

These are set in travis CI, and via a file named `.env` in the project root dir for deployments.

## Important note
Spotify does not distribute your entire listening history. At any one point in time, Spotify will tell you the last 50 tracks that you have listened to. That is why this repo polls the endpoint and saves the data. Your listening history data grows exponentially more valuable with time, so you cannot make interesting playlists as soon as you install this application. Personally, I created the `save-recently-played` functionality cron first, and it ran for almost 1 year before I implemented the parser and the puppeted installation. 

## Where is the magic?
I'm so glad you asked! It is in `recently_played_playlists/db/db.py`:
```
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
if filter_args['comparator'] != -1 and filter_args['count'] != -1:
    order_by = get_order_by(filter_args['comparator'])
    comparator = str_of_comparator(filter_args['comparator'])
    query += f" WHERE num_plays {comparator} {filter_args['count']} ORDER BY num_plays {order_by}"

# If limit was not set to default value, so add it to query.
if filter_args['limit'] != -1:
    query += ' LIMIT {limit}'.format(limit=filter_args['limit'])

```
The basis of a playlist is this query. The parser allows for playlists to be composed of an `and` of playlists, `or` of playlists, or a `diff` of playlists. There is no restriction to how many playlists can be evaluated to generate a single playlist.

Example: 
- Top 100 most played from Jan 1 2016 to Jan 1 2017, that are not saved in my library

More complicated example:
- Top 100 most played from Jan 1 2016 to Jan 1 2017 AND Songs played < 3 times from Jan 1 2017 to Jan 1 2018.
  - Your most played in 2016, that you seem to have forgotten about in 2017!

## What other types of query filters are supported?
See the README in the [recently-played-playlists-parser](https://github.com/ndelnano/recently-played-playlists-parser)

## Have ideas on what else could be done?
I'd love to hear them! See the README in the [recently-played-playlists-parser](https://github.com/ndelnano/recently-played-playlists-parser) for my ideas, and send me any via an issue....or pull request ;)

# Why don't you run this as a service?
- Listening history data becomes interesting when there's lots of it (or when its far in the past), and lots of data (or storing it for decades) means higher cloud computing costs. 

My $5/mo DigitalOcean droplet supports me and 4 friends, but it wouldn't support 100 or 1000 people.

# Could I do this Apple music?
Probably! I didn't write this project generically because:
- Apple requires you to be a member of their developer program to hit the Apple music recently played API endpoint :/
- Soundcloud doesn't have a similar endpoint, so I only saw myself using this for Spotify.

It would be super easy to do! If you're interested in adding Apple music support let me know! I'd be willing to help.
