[![Build Status](https://travis-ci.org/ndelnano/recently-played-playlists.svg?branch=master)](https://travis-ci.org/ndelnano/recently-played-playlists)

# About
This repo holds various functionalities for supporting the [recently-played-playlists-parser](https://github.com/ndelnano/recently-played-playlists-parser).
- Utilites for fetching a Spotify user's recently played tracks from the spotify API and saving them in MySQL.
  - Poll spotify's [get-recently-played endpoint](https://developer.spotify.com/documentation/web-api/reference/player/get-recently-played/) and save new track plays to MySQL. I poll this API endpoint as a cron to preserve my listening history.
  - Save various track data not included in the get-recently-played endpoint by calling the [get-several-tracks endpoint](https://developer.spotify.com/documentation/web-api/reference/tracks/get-several-tracks/) Currently, this is in development for adding the `release_date` attribute to each track.
- HTTP API for supporting queries from playlist-parser
  - `/process_filter` -- Transform a `Playlist` (list of filters) into an SQL query, execute it, and return a list of spotify `track_id`'s. For what is possible, see recently-played-playlists-parser.
  - `/make_playlist` -- Create a playlist, given a list of spotify `track_id`'s.

You should not care to interact with the API yourself -- you should use the recently-played-playlists-parser.

# Installing and running
See [recently-played-playlists-puppet](https://github.com/ndelnano/recently-played-playlists-puppet) for a puppet module and detailed instructions.

## Setting up developer environment
The acceptance tests use MySQL. You can either:
- Clone this repo, install tox, and develop unit tests while relying on travisci for running acceptance tests
- Use puppeted installation docs to run MySQL, do the above steps, and add a .env file

Note -- I don't have spotify tokens for development / testing ;( You'll want to use your own. See the puppet installation docs for how to generate them.

## Environment variables
This list serves as documentation. If you are installing, you really want to use the puppet repo and its instructions.

- SPOTIFY_CLIENT_ID
- SPOTIFY_CLIENT_SECRET
- DB_HOST
- DB_USER
- DB_PASS
- DB_NAME
- FLASK_APP

These are set in travis CI, and via a file named `.env` in the root project dir for deployments.

## Running the code
Two subcommands are implemented. See [recently_played_playlists/cli/main.py](https://github.com/ndelnano/recently-played-playlists/blob/master/recently_played_playlists/cli/main.py).
- recently-played-playlists save-played-tracks
- recently-played-playlists api

In the puppeted installation, `save-played-tracks` is run as a cron, and `api` is run as a systemd service.

## Important note
Spotify does not distribute your entire listening history. At any one point in time, Spotify will tell you the last 50 tracks that you have played. That is why this repo polls the endpoint and saves the data. Sadly, you won't be able to make interesting playlists immediately after you install this application -- it will take some time to have enough data.

## Where is the magic?
I'm so glad you asked! It's in [recently_played_playlists/db/db.py](https://github.com/ndelnano/recently-played-playlists/blob/master/recently_played_playlists/db/db.py):
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

# If limit is set, add it to the query.
if filter_args['limit'] != -1:
    query += ' LIMIT {limit}'.format(limit=filter_args['limit'])

```
This query is the basis of a playlist. The parser allows for playlists to be composed of an `and` of playlists, an `or` of playlists, or a `diff` of playlists. There is no restriction to how many playlists can be evaluated to generate a single playlist.

Example: 
- Top 100 most played from Jan 1 2016 to Jan 1 2017 that are not saved in my library

More complicated example:
- Top 100 most played from Jan 1 2016 to Jan 1 2017 AND Songs played < 3 times from Jan 1 2017 to Jan 1 2018.
  - Your most played in 2016, that you seem to have forgotten about in 2017!

## What other filtering can be done?
See the README in the [recently-played-playlists-parser](https://github.com/ndelnano/recently-played-playlists-parser) for all supported filters.

## Have ideas for other filters?
I'd love to hear! See the README in the [recently-played-playlists-parser](https://github.com/ndelnano/recently-played-playlists-parser) for my ideas, and send me any of your own via an issue....or pull request ;)

# Why don't you run this as a service?
Listening history data becomes interesting when there's lots of it (or when its far in the past), and lots of data (or storing it for decades) means higher cloud computing costs. 

My $5/mo DigitalOcean droplet supports me and 4 friends, but it wouldn't support 100 or 1000 people.

# What about Apple Music or Soundcloud?
- Apple requires you to be a member of their developer program to hit their recently played API endpoint, which costs $$ :/
- Soundcloud doesn't have a similar endpoint
