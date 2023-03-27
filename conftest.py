import secrets

import pytest
import requests

from infra import api_communication as api
from logic import endpoints, User, Playlist, Song, Voting
from utils import logger
from config import Config


def pytest_addoption(parser):
    parser.addoption("--host",
                     action="store",
                     default="http://127.1.1.0",
                     help="host url")
    parser.addoption("--port",action="store"
                     ,default="3002",
                     help="port")


@pytest.fixture(scope="session")
def configuration(pytestconfig):
    host = pytestconfig.getoption("host")
    port = pytestconfig.getoption("port")
    conf = Config(host, port)
    yield conf


@pytest.fixture(scope="session")
def init_session():
    with requests.session() as s:
        logger.log("Session started")
        s.headers.update({"accept": "application/json"})
        con = api.Communication(s)
        yield con
    logger.log("Session Closed", con.session)


@pytest.fixture(scope="session")
def users(init_session, configuration):
    return endpoints.UsersAPI(init_session, configuration)


@pytest.fixture(scope="session")
def songs(init_session, configuration):
    return endpoints.SongsAPI(init_session, configuration)


@pytest.fixture(scope="session")
def playlists(init_session, configuration):
    return endpoints.PlaylistsAPI(init_session, configuration)
@pytest.fixture(scope="session")
def admin(init_session,configuration):
    return endpoints.AdminAPI(init_session, configuration)
@pytest.fixture
def setup_teardown(admin):

    admin.delete_all_users()
    admin.delete_all_song()
    logger.log("<setup> Cleared all users from DB")
    yield
    del admin


@pytest.fixture
def set_up_user(users) -> User:
    user = User.create_randomly()
    assert users.add_user(user).data == user.user_name, "adding user function failed"
    return user


@pytest.fixture
def set_up_playlist(set_up_user, users) -> Playlist:
    playlist = Playlist(user_name=set_up_user.user_name, user_password=set_up_user.user_password,
                        playlist_name="2020 pop hits")
    users.add_playlist(playlist)
    return playlist


@pytest.fixture
def set_up_song(songs) -> Song:
    song = Song("pop", "adi", "israel vibes", 2020)
    songs.add_song(song)
    return song


@pytest.fixture
def setup_songs(admin,songs,users,playlists):
    users_ = [User.create_randomly() for _ in range(10)]
    songs_ = [Song.create_randomly()
             for _ in range(30)]
    playlists_ = [Playlist.create_randomly() for _ in range(5)]
    [songs.add_song(s) for s in songs_]
    [users.add_user(u) for u in users_]

    for i,song in enumerate(songs_):
        p = secrets.choice(playlists_)
        u = secrets.choice(users_)
        u2 = secrets.choice(users_)

        while u == u2:
            u2 = secrets.choice(users_)
        vote = Voting(p.playlist_name,
                      song.song_title,**u.as_json())
        vote2 = Voting(p.playlist_name,
                      song.song_title, **u2.as_json())
        if i < 11:
            songs.upvote(vote)
            songs.upvote(vote2)
        elif i in range(11,21):
            songs.upvote(vote)
        else:
            pass


