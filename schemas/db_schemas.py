
from dataclasses import dataclass


class BaseSchema:
    """Base interface for DB schemas"""
    def as_json(self) -> dict:
        """convert object to dictionary/json type"""
        return self.__dict__

    def __eq__(self, other):
        """Generic compare method for all db schemas"""
        if not type(other) == type(self):
            return False
        for k,v in self.__dict__.items():
            if getattr(other,k) != v:
                return False
        return True



@dataclass
class Song(BaseSchema):
    """Represent Song schema"""
    song_genre:str
    song_performer:str
    song_title:str
    song_year:int

@dataclass
class SongResponse(BaseSchema):
    """Represent Song Response Schema"""
    genre: str
    performer: str
    rating: int
    title: str
    year: int

@dataclass
class Playlist(BaseSchema):
    """Represent Playlist Schema"""
    playlist_name:str
    user_name :str
    user_password :str

@dataclass
class Voting(BaseSchema):
    """Represent Voting schema"""
    playlist_name :str
    song_title :str
    user_name :str
    user_password :str

@dataclass
class User(BaseSchema):
    """Represent User schema"""
    user_name :str
    user_password :str

@dataclass
class UserResponse(BaseSchema):
    """Represent User Response schema"""
    friends: list
    playlists: list
    user_name: str

@dataclass
class Friend(BaseSchema):
    """Represent Friend schema"""
    friend_name:str
    user_name :str
    user_password :str


@dataclass
class Password(BaseSchema):
    """Represent Password schema"""
    user_name :str
    user_new_password :str
    user_password :str


