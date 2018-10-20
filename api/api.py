import spotify.util

from flask import Flask
from flask import request

app = Flask(__name__)

# TODO: add validation? Probably more useful to add validation to what sends
# to the playlist-parser and trust that. Everything here is a string.
@app.route('/process_filter')
def process_filter():
    '''
    Processes a filter according to the playlist-parser spec and returns a list of
    spotify `song_id` that satisfy the filter.
    '''
    filter_args = dict()
    filter_args['username'] = request.args.get('username')
    filter_args['time_begin'] = request.args.get('time_begin')
    filter_args['time_end'] = request.args.get('time_end')
    filter_args['agby'] = request.args.get('agby')
    filter_args['limit'] = int(request.args.get('limit'))
    filter_args['saved'] = int(request.args.get('saved'))
    filter_args['count'] = int(request.args.get('count'))
    filter_args['comparator'] = int(request.args.get('comparator'))
    filter_args['release_start'] = request.args.get('release_start')
    filter_args['release_end'] = request.args.get('release_end')
    return spotify.util.process_playlist(filter_args)

@app.route('/test', methods=['POST'])
def test():
    print('request.data')
    print(request.data)
    print('request.form')
    print(request.form)
    return ''

# TODO
@app.route('/make_playlist', methods=['POST'])
def make_playlist():
    pass
