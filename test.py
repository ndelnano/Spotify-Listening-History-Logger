import spotify.util

tracks = ['1', '2', '3', '4']
bools = [True, False, True, False]
expected = ['1', '3']
assert (spotify.util.filter_lists_based_on_value(True, tracks, bools) == expected)
