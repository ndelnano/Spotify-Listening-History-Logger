from setuptools import setup

setup(
    name='recently-played-playlists',
    version='0.0.0',
    description='Poll Spotify listening history and log to MySQL, & HTTP API for recently-played-playlists-parser.',
    author="@ndelnano",
    author_email="nickdelnano@gmail.com",
    url='github.com/ndelnano/recently-played-playlists',
    install_requires=[
        'flask',
        'mysqlclient',
        'python-dotenv',
        'ndelnano-spotipy',
    ],
    license='LICENSE.txt',
    packages=['spotify', 'db']
)
