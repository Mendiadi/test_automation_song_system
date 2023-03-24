import allure

from config import Config
from infra import Communication
from logic import (
    User,
    UserResponse,
    Password,
    BaseResponse,
    Playlist,
    Friend
)


class BaseAPI:
    """Base class to share functionality"""

    def __init__(self, communication: Communication, config: Config):
        self.conn = communication
        self.base_url = f"{config.HOST}:{config.PORT}/"


class AdminAPI(BaseAPI):
    def __init__(self, session, config):
        super().__init__(session, config)
        self.base_url += "admin"

    def delete_all_users(self):
        return self.conn.delete(f"{self.base_url}/delete_all_users").json()


class UsersAPI(BaseAPI):
    """API for interactions with users"""

    def __init__(self, session, config):
        super().__init__(session, config)
        self.base_url += "users"

    def add_user(self, user: User) -> BaseResponse:
        """
        Perform post requests for add new user top the server
        :param user: User object DB schema
        :return: dict of msg if success and the username
        """
        with allure.step(f"add user {user}"):
            r = self.conn.post(f"{self.base_url}/add_user", json=user.as_json())
        return BaseResponse.create_from_response(r)

    def get_user(self, user_name: str) -> UserResponse:
        """
        Fetching the user by get requests to the server
        :param user_name: username you want to fetch as string
        :return: UserResponse object
        """
        with allure.step(f"getting the user {user_name}"):
            r = self.conn.get(f"{self.base_url}/get_user", params={"user_name": user_name})
        return UserResponse.create_from_response(r)

    def get_playlist(self, playlist: Playlist
                     ) -> BaseResponse:
        """
        Perform get request to the server,
        fetching the playlist by the object
        :param playlist: Playlist object DB schema
        :return: common response
        """
        ...

    def change_password(self, password: Password) -> UserResponse:
        """
        Perform put requests to the server,
        change the password for given username.
        :param password: password object schema
        :return: UserResponse object
        """
        with allure.step(f"change password {password}"):
            r = self.conn.put(f"{self.base_url}/change_password", json=password.as_json())
        return UserResponse.create_from_response(r)
    def add_friend(self, friend: Friend) -> BaseResponse:
        """
         Perform put requests to the server,
         add friend to user.
         :param friend: db schema
         :return: common response
         """
        ...

    def add_playlist(self, playlist: Playlist) -> BaseResponse:
        """
        Perform post requests to server
        adding new playlist to user.
        :param playlist: db schema
        :return: common response
        """
        ...


class SongsAPI(BaseAPI):
    """API for interactions with songs"""
    ...


class PlaylistsAPI(BaseAPI):
    """API for interaction with playlists"""
    ...
