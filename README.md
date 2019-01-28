[![Build Status](https://travis-ci.org/ndelnano/recently-played-playlists.svg?branch=master)](https://travis-ci.org/ndelnano/recently-played-playlists)

This repo holds various functionalities for supporting the [recently-played-playlists-parser](https://github.com/ndelnano/playlist-parser).
* Utilites for saving data of a user's recently played tracks from the spotify API and inserting them into MySQL
  * Poll spotify's [get-recently-played endpoint](https://developer.spotify.com/documentation/web-api/reference/player/get-recently-played/) and save this data (intended to be run as cron.. TODO see [recently-played-playlists-puppet](https://github.com/ndelnano/recently-played-playlists-puppet).
  * Save various song data not included in the get-recently-played endpoint by calling the [get-several-tracks](https://developer.spotify.com/documentation/web-api/reference/tracks/get-several-tracks/) endpoint TODO
* HTTP API for supporting queries from playlist-parser
  * /process_filter TODO add parameters -- returns tracks that match the filter
  * /make_playlist TODO add parameters -- create playlist with supplied tracks


Current setup instructions: (will be useful when completing puppeted setup)
git clone __this_repo__
sudo apt-get install tox python3.6-dev libmysqlclient-dev
tox -e flask

sudo apt install mysql-server
sudo mysql_secure_installation


TODO: document moving .env file into place after `pip3 installing recently-played-playlists`

## Environment variables
- SPOTIFY_CLIENT_ID
- SPOTIFY_CLIENT_SECRET
- DB_HOST
- DB_USER
- DB_PASS
- DB_NAME
- FLASK_APP

These are set in travis CI, and via a .env file in the project root dir for deployments.

## Could I do this Apple music?
Probably! I didn't write this project generically because:
- Apple requires you to be a member of their developer program to hit the Apple music recently played API endpoint :/
- Soundcloud doesn't have a similar endpoint, so I only saw myself using this for Spotify.
- Laziness -- it would be super easy to do! If you're interested in adding Apple music support let me know! I'd be willing to help.

## What type of playlists can I make with this?
See the README in the [recently-played-playlists-parser](github.com/ndelnano/recently-played-playlists-parser)
