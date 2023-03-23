from infra.api_communication import Communication
from schemas.db_schemas import (
    User,
    UserResponse,
    Password,
    Playlist
)
class BaseAPI:
    """Base class to share functionality"""
    def __init__(self,communication:Communication):
        self.communication = communication

class UsersAPI(BaseAPI):
    """API for interactions with users"""

    def add_user(self,user:User) -> dict:
        """
        Perform post requests for add new user top the server
        :param user: User object DB schema
        :return: dict of msg if success and the username
        """
        ...


    def get_user(self,user_name:str) -> UserResponse:
        """
        Fetching the user by get requests to the server
        :param user_name: username you want to fetch as string
        :return: UserResponse object
        """
        ...

    def get_playlist(self,playlist:Playlist
                     ) -> dict:
        """
        Perform get request to the server,
        fetching the playlist by the object
        :param playlist: Playlist object DB schema
        :return: todo
        """
        ...

    
    def change_password(self,password:Password) -> UserResponse:
        """
        Perform put requests to the server,
        change the password for given username.
        :param password: password object schema
        :return: UserResponse object
        """
        ...

class SongsAPI(BaseAPI):
    """API for interactions with songs"""
    ...


class PlaylistsAPI(BaseAPI):
    """API for interaction with playlists"""
    ...


