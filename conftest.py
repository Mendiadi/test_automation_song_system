import pytest
import requests


from infra import api_communication as api
from logic import endpoints,User
from utils import logger
from config import Config

def pytest_addoption(parser):
    parser.addoption("--host",
                     action="store",
                     default="http://192.168.1.33",
                     help="host url")


@pytest.fixture(scope="session")
def configuration(pytestconfig):
    host = pytestconfig.getoption("host")
    conf = Config(host, "3002")
    yield conf


@pytest.fixture(scope="session")
def init_session():
    with requests.session() as s:
        logger.log("Session started")
        s.headers.update({"accept": "application/json"})
        con = api.Communication(s)
        yield con
    logger.log("Session Closed", con.session)


@pytest.fixture
def users(init_session, configuration):
    return endpoints.UsersAPI(init_session, configuration)


@pytest.fixture
def songs(init_session, configuration):
    return endpoints.SongsAPI(init_session, configuration)


@pytest.fixture
def playlists(init_session, configuration):
    return endpoints.PlaylistsAPI(init_session, configuration)


@pytest.fixture
def setup_teardown(init_session, configuration):
    endpoints.AdminAPI(init_session, configuration).delete_all_users()
    logger.log("<setup> Cleared all users from DB")
    yield

@pytest.fixture
def set_up_user(users):
    user = User.create_randomly()
    assert users.add_user(user).data == user.user_name, "adding user function failed"
    return user