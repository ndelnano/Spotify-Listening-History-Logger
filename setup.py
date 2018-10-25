from setuptools import setup

setup(
    name='rpp-collector',
    version='0.0.0',
    description='Collect spotify listening history',
    author="@ndelnano",
    author_email="nickdelnano@gmail.com",
    url='',
    install_requires=[
        'flask',
        'mysqlclient',
        'python-dotenv',
        'ndelnano-spotipy',
    ],
    license='LICENSE.txt',
    packages=['spotify, db']
)
