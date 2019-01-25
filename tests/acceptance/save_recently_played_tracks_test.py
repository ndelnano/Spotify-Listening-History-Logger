from db.db import get_all_users
from spotify.save_recently_played_tracks import call_recently_played_endpoint

def test_call_recently_played_endpoint():
    test_user = get_all_users()[0]
    assert call_recently_played_endpoint(test_user) != None
