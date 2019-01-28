from recently_played_playlists.db.db import str_of_comparator
from recently_played_playlists.db.db import get_order_by

def test_str_of_comparator():
    assert str_of_comparator(0) == "<"
    assert str_of_comparator(1) == "<="
    assert str_of_comparator(2) == ">"
    assert str_of_comparator(3) == ">="

def test_get_order_by():
    assert get_order_by(0) == 'ASC'
    assert get_order_by(1) == 'ASC'

    assert get_order_by(2) == 'DESC'
    assert get_order_by(3) == 'DESC'
