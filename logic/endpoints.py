from typing import Callable, Any

import allure

from config import Config
from infra import Communication
from logic import (
    User,
    UserResponse,
    Password,
    BaseResponse,
    Playlist,
    Friend,
    BaseSchema

)
from logic.data import UrlPaths as url_


class BaseAPI:
    """Base class to share functionality"""

    def __init__(self, communication: Communication, config: Config):
        self.conn = communication
        self.base_url = f"{config.HOST}:{config.PORT}/"

    def _response(self, instance: [BaseResponse, BaseSchema],
                  conn: Callable,
                  url: str, step: str, **options) -> [BaseResponse, BaseSchema, Any]:
        with allure.step(step):
            r = conn(f"{self.base_url}{url}", **options)
        return instance.create_from_response(r)


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
        return self._response(BaseResponse, self.conn.post,
                              url_.add_user, f"add user {user}", json=user.as_json())

    def get_user(self, user_name: str) -> UserResponse:
        """
        Fetching the user by get requests to the server
        :param user_name: username you want to fetch as string
        :return: UserResponse object
        """
        return self._response(UserResponse, self.conn.get, url_.get_user,
                              f"getting the user {user_name}", params={"user_name": user_name})

    def get_playlist(self, playlist: Playlist
                     ) -> Playlist:
        """
        Perform get request to the server,
        fetching the playlist by the object
        :param playlist: Playlist object DB schema
        :return: common response
        """
        return self._response(Playlist, self.conn.get, url_.get_playlist
                              , f"getting the playlist {playlist}", params=playlist.as_json())

    def change_password(self, password: Password) -> UserResponse:
        """
        Perform put requests to the server,
        change the password for given username.
        :param password: password object schema
        :return: UserResponse object
        """
        return self._response(UserResponse, self.conn.put, url_.change_password
                              , f"change password {password}", json=password.as_json())

    def add_friend(self, friend: Friend) -> BaseResponse:
        """
         Perform put requests to the server,
         add friend to user.
         :param friend: db schema
         :return: common response
         """
        return self._response(BaseResponse, self.conn.put, url_.add_friend,
                              f"add friend {friend}", json=friend.as_json())

    def add_playlist(self, playlist: Playlist) -> BaseResponse:
        """
        Perform post requests to server
        adding new playlist to user.
        :param playlist: db schema
        :return: common response
        """
        return self._response(BaseResponse, self.conn.post, url_.add_playlist
                              , f"add playlist {playlist}", json=playlist.as_json())


class SongsAPI(BaseAPI):
    """API for interactions with songs"""
    ...


class PlaylistsAPI(BaseAPI):
    """API for interaction with playlists"""
    ...
