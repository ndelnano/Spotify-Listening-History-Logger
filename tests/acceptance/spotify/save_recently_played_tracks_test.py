import re

from recently_played_playlists.db.db import get_all_users
from recently_played_playlists.spotify.save_recently_played_tracks import call_recently_played_endpoint
from recently_played_playlists.spotify.util import get_spotify_client_for_username

def test_call_recently_played_endpoint():
    test_user = get_all_users()[0]

    # Assert we got the number of tracks expected
    tracks = call_recently_played_endpoint(test_user)
    assert len(tracks) == 50
    
    # Assert that a track has all the expected fields
    track = tracks[0]
    assert track['name'] is not None
    assert track['uri'] is not None
    assert track['id'] is not None
    assert track['duration_ms'] is not None
    assert track['played_at'] is not None

'''This is a regression test as I had to work around
    spotify's timestamp format in order to parse it.
    See documentation in spotify/save_recently_played_tracks.py 
    iso_8601_timestamp_with_millis_and_timezone_to_seconds_since_epoch

    Spotify returns 'played_at' in this form. `2004-06-03T12:34:56.123Z`
'''
def test_timestamp_format_of_played_at(): 
    spotify = get_spotify_client_for_username('test_user')
    response = spotify.current_user_recently_played()

    # The structure of the response is confusing, copied this from
    # spotify/save_recently_played_tracks.py
    for k, api_response_tracks in response.items():
        if k == 'items':
            for api_response_track in api_response_tracks:
                # Only do the assertion once
                assert re.search(r'\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d.\d\d\dZ', api_response_track['played_at']) is not None
                break

