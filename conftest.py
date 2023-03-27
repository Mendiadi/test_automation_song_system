import secrets
import pytest
import requests

import utils
from infra import api_communication as api
from logic import endpoints, User, Playlist, Song, Voting
from utils import logger
from config import Config


def pytest_addoption(parser):
    """Adding CLI arguments for host and port"""
    parser.addoption("--host",
                     action="store",
                     default="http://127.1.1.0",
                     help="host url")
    parser.addoption("--port", action="store"
                     , default="3002",
                     help="configure port")


@pytest.fixture(scope="session")
def configuration(pytestconfig):
    """Grab the options and store at config object"""
    host = pytestconfig.getoption("host")
    port = pytestconfig.getoption("port")
    conf = Config(host, port)
    yield conf


@pytest.fixture(scope="session")
def init_session():
    """Initials new session
        runs only once per test session."""
    with requests.session() as s:
        logger.log("Session started")
        s.headers.update({"accept": "application/json"})
        con = api.Communication(s)
        yield con
    logger.log("Session Closed", con.session)


@pytest.fixture(scope="session")
def users(init_session, configuration):
    """Wrapper for users API"""
    return endpoints.UsersAPI(init_session, configuration)


@pytest.fixture(scope="session")
def songs(init_session, configuration):
    "Wrapper for songs API"
    return endpoints.SongsAPI(init_session, configuration)


@pytest.fixture(scope="session")
def playlists(init_session, configuration):
    """Wrapper for playlists API"""
    return endpoints.PlaylistsAPI(init_session, configuration)


@pytest.fixture(scope="session")
def admin(init_session, configuration):
    """Wrapper for admin API"""
    return endpoints.AdminAPI(init_session, configuration)


@pytest.fixture
def setup_teardown(admin):
    """Remove all data from DB"""
    admin.delete_all_users()
    admin.delete_all_song()
    logger.log("<setup> Cleared all data from DB")
    yield


@pytest.fixture
def set_up_user(users) -> User:
    """Create User and add to the DB"""
    user = User.create_randomly()
    users.add_user(user)
    return user


@pytest.fixture
def set_up_playlist(set_up_user, users) -> Playlist:
    """Create playlist and add to DB"""
    playlist = Playlist(user_name=set_up_user.user_name, user_password=set_up_user.user_password,
                        playlist_name="2020 pop hits")
    users.add_playlist(playlist)
    return playlist


@pytest.fixture
def set_up_song(songs) -> Song:
    """Create song and add to DB"""
    song = Song("pop", "adi", "israel vibes", 2020)
    songs.add_song(song)
    return song


@pytest.fixture
def setup_songs(admin, songs, users, playlists):
    """Create users and songs give rating and add to db"""
    users_ = utils.obj_sequence(User.create_randomly, 10)
    songs_ = utils.obj_sequence(Song.create_randomly, 30)
    playlists_ = utils.obj_sequence(Playlist.create_randomly, 5)
    utils.obj_sequence(songs.add_song, sequence=songs_)
    utils.obj_sequence(songs.add_song, sequence=users_)
    for i, song in enumerate(songs_):
        p = secrets.choice(playlists_)
        u = secrets.choice(users_)
        u2 = secrets.choice(users_)
        while u == u2:
            u2 = secrets.choice(users_)
        vote = Voting(p.playlist_name,
                      song.song_title, **u.as_json())
        vote2 = Voting(p.playlist_name,
                       song.song_title, **u2.as_json())
        if i < 11:
            songs.upvote(vote)
            songs.upvote(vote2)
        elif i in range(11, 21):
            songs.upvote(vote)
        else:
            ...
