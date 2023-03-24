import pytest
import requests
from infra import api_communication as api
from logic import endpoints
from utils import logger
from config import Config

def pytest_addoption(parser):
    parser.addoption("--host",
                     action="store",
                     default="localhost",
                     help="host url")

@pytest.fixture(scope="session")
def configuration():
    conf = Config("http://127.0.0.1","3002")
    yield conf

@pytest.fixture(scope="session")
def init_session():
    with requests.session() as s:
        logger.log("Session started")
        s.headers.update({"accept":"application/json"})
        con = api.Communication(s)
        yield con
    logger.log("Session Closed",con.session)

@pytest.fixture
def users(init_session,configuration):
    return endpoints.UsersAPI(init_session,configuration)


@pytest.fixture
def songs(init_session,configuration):
    return endpoints.SongsAPI(init_session,configuration)

@pytest.fixture
def playlists(init_session,configuration):
    return endpoints.PlaylistsAPI(init_session,configuration)


@pytest.fixture
def setup_teardown(init_session,configuration):
    endpoints.AdminAPI(init_session,configuration).delete_all_users()
    logger.log("<setup> Cleared all users from DB")
    yield
