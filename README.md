This repo holds various functionalities for supporting the [playlist-parser](https://github.com/ndelnano/playlist-parser).
* Utilites for saving data of a user's recently played tracks from the spotify API and inserting them into MySQL
  * Poll spotify's [get-recently-played endpoint](https://developer.spotify.com/documentation/web-api/reference/player/get-recently-played/) and save this data (intended to be run as cron.. TODO see [recently-played-playlists-puppet](https://github.com/ndelnano/recently-played-playlists-puppet).
  * Save various song data not included in the get-recently-played endpoint by calling the [get-several-tracks](https://developer.spotify.com/documentation/web-api/reference/tracks/get-several-tracks/) endpoint TODO
* HTTP API for supporting queries from playlist-parser
  * /process_filter TODO add parameters -- returns tracks that match the filter
  * /make_playlist TODO add parameters -- create playlist with supplied tracks

