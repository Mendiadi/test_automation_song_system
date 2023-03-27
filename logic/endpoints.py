from typing import Callable, Any, Literal
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
    BaseSchema,
    Song,
    SongResponse,
    Voting

)
from logic.data import UrlPaths as url_


class BaseAPI:
    """Base class to share functionality"""

    def __init__(self, communication: Communication, config: Config):
        self.conn = communication
        self.base_url = f"{config.HOST}:{config.PORT}/"

    def _fetch(self, instance: [BaseResponse, BaseSchema],
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

    def delete_all_song(self):
        return self.conn.delete(f"{self.base_url}/delete_all_songs").json()

    def set_songs(self, songs: list[Song]):
        return self.conn.post(f"{self.base_url}/set_songs",
                              json=[song.as_json() for song in songs])

    def set_users(self, users: list[User]):
        return self.conn.post(f"{self.base_url}/set_users",
                              json=[user.as_json() for user in users])


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
        return self._fetch(BaseResponse, self.conn.post, url_.add_user, f"add user {user}", json=user.as_json())

    def get_user(self, user_name: str) -> UserResponse:
        """
        Fetching the user by get requests to the server
        :param user_name: username you want to fetch as string
        :return: UserResponse object
        """
        return self._fetch(UserResponse, self.conn.get, url_.get_user, f"getting the user {user_name}",
                           params={"user_name": user_name})

    def get_playlist(self, playlist: Playlist
                     ) -> list[SongResponse]:
        """
        Perform get request to the server,
        fetching the playlist by the object
        :param playlist: Playlist object DB schema
        :return: common response
        """
        r = self._fetch(BaseResponse, self.conn.get, url_.get_playlist, f"getting the playlist {playlist}",
                        params=playlist.as_json())
        return [SongResponse(**song) for song in r.data] if r.data or r.data == [] else r

    def change_password(self, password: Password) -> UserResponse:
        """
        Perform put requests to the server,
        change the password for given username.
        :param password: password object schema
        :return: UserResponse object
        """
        return self._fetch(UserResponse, self.conn.put, url_.change_password, f"change password {password}",
                           json=password.as_json())

    def add_friend(self, friend: Friend) -> BaseResponse:
        """
         Perform put requests to the server,
         add friend to user.
         :param friend: db schema
         :return: common response
         """
        return self._fetch(BaseResponse, self.conn.put, url_.add_friend, f"add friend {friend}", json=friend.as_json())

    def add_playlist(self, playlist: Playlist) -> BaseResponse:
        """
        Perform post requests to server
        adding new playlist to user.
        :param playlist: db schema
        :return: common response
        """
        return self._fetch(BaseResponse, self.conn.post, url_.add_playlist, f"add playlist {playlist}",
                           json=playlist.as_json())


class SongsAPI(BaseAPI):
    """API for interactions with songs"""

    def __init__(self, session, config):
        super().__init__(session, config)
        self.base_url += "songs"

    def add_song(self, song: Song) -> BaseResponse:
        """
        Perform post requests to server
        add song to the system
        :param song: ew song schema
        :return: common response schema
        """
        return self._fetch(BaseResponse, self.conn.post, url_.add_song, f"adding song {song} to the system",
                           json=song.as_json())

    def get_song(self, song_title: str) -> SongResponse:
        """
        Perform get request to server
        getting the song by title
        :param song_title: string representing title of song
        :return Song response schema
        """
        return self._fetch(SongResponse, self.conn.get, url_.get_song, f"getting the song {song_title}",
                           params={"song_title": song_title})

    def downvote(self, vote: Voting) -> BaseResponse:
        """
        Perform put requests to server
        downvote the rating.
        :param vote: voting object
        :return: Schema Response
        """
        return self._fetch(BaseResponse, self.conn.put, url_.downvote,
                           f"downvote to {vote}", json=vote.as_json())

    def upvote(self, vote: Voting) -> BaseResponse:
        """
           Perform put requests to server
           upvote the rating.
           :param vote: voting object
           :return: Schema Response
       """
        return self._fetch(BaseResponse, self.conn.put, url_.upvote,
                           f"upvote to {vote}", json=vote.as_json())

    def ranked_songs(self, op: Literal["less", "eq", "greater"], rank: str):
        """
        Perform get request to server
        fetching the songs by ranks
        :param op: equal, greater, or less then rate value
        :param rank: amount of rate to operate with
        :return: list of songs
        """
        r = self._fetch(BaseResponse, self.conn.get,
                        url_.ranked_songs, f"getting ranked songs op={op} rate={rank}",
                        params={"op": op, "rank": rank})
        if r.data or r.data == []:

            yield [song for song in r.data]
        else:
            return r


class PlaylistsAPI(BaseAPI):
    """API for interaction with playlists"""

    def __init__(self, session, config):
        super().__init__(session, config)
        self.base_url += "playlists"

    def add_song(self, song: Song, playlist: Playlist) -> BaseResponse:
        """
        Perform post requests to server
        add song to playlist
        :param song: song schema data to add
        :return: common response
        """
        return self._fetch(BaseResponse, self.conn.post, url_.add_song, f"adding song {song} to {playlist}",
                           json=playlist.as_add_song_schema(song.song_title).as_json())
