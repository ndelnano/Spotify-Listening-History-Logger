from spotify import save_recently_played_tracks

def test_iso_8601_timestamp_with_millis_and_timezone_to_seconds_since_epoch():
    sample_timestamp_from_spotify_api = '2016-12-13T20:44:04.589Z'
    expected_unix_time = 1481661844
    assert save_recently_played_tracks.iso_8601_timestamp_with_millis_and_timezone_to_seconds_since_epoch(sample_timestamp_from_spotify_api) == expected_unix_time

def test_find_latest_timestamp():
    latest_timestamp = 3000000000
    tracks = list(dict())
    tracks.append({'played_at': 1000000000})
    tracks.append({'played_at': 3000000000})
    tracks.append({'played_at': latest_timestamp})
    assert save_recently_played_tracks.find_latest_timestamp(tracks) == latest_timestamp
