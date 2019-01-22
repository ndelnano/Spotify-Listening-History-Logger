from spotify.util import get_spotify_client_for_username
from db.db import get_time_of_last_track_play

def save_recently_played_tracks(username):
    '''
    Spotify does support an 'after' timestamp on the get-recently-played endpoint, however, if no songs have been played since 'after', spotify returns 1 song, the most recently played one for the user. For this reason, do not use the 'after' parameter, and use the `spotify_time_of_last_track_played` field in the database to determine whether the song is 'new' or not.
    '''
    spotify = get_spotify_client_for_username(username)
    tracks = spotify.current_user_recently_played()

    time_of_last_track_play = get_time_of_last_track_play(username)

    for track in tracks:
        print(track)
    print('Time of last track play in database: ')
    print(time_of_last_track_play)

