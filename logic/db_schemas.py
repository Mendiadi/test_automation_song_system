from dataclasses import dataclass

from utils import get_generic_random_schema


class BaseSchema:
    """Base interface for schemas"""

    def __init__(self, **kwargs):
        """just for pep8 hints"""
        ...

    def as_json(self) -> dict:
        """convert object to dictionary/json type"""
        return self.__dict__

    @classmethod
    def create_randomly(cls, **data):
        """Create instant randomly generic method
            * you can add kwargs arguments to provide
             manual values for better performance *"""
        attrs, manual = [], {}
        for field in cls.__dict__["__dataclass_fields__"].values():
            field.default, field.default_factory = None, None
            val = data.get(field.name, None)
            if not val:
                attrs.append((field.name, field.type))
            else:
                manual[field.name] = val
        return get_generic_random_schema(attrs, manual, cls)

    @classmethod
    def create_from_response(cls, response):
        """Create instant for the child class generic calls
            by the response"""
        if not response:
            raise Exception("Test failed. Connection failure.")
        r = BaseResponse(**response.json())
        print(r)
        return r if getattr(r, "error") or cls == type(r) or not r.data else cls(**r.data)

    def __eq__(self, other):
        """Generic compare method for all db schemas"""
        if type(other) != type(self):
            return False
        for k, v in self.__dict__.items():
            if getattr(other, k) != v:
                return False
        return True

    def __str__(self) -> str:
        """That How Schema Should Convert to String"""
        return str(self.as_json())

    def __repr__(self) -> str:
        """Override the magic function
        to enable print to stdout"""
        return str(self)


class BaseResponse(BaseSchema):
    """Generic Base class for Responses"""

    def __init__(self, **kw):
        super().__init__()
        self.__dict__.update(kw)

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def __getattr__(self, item):
        return self.__dict__.get(item)


@dataclass
class Song(BaseResponse):
    """Represent Song schema"""
    song_genre: str
    song_performer: str
    song_title: str
    song_year: int


@dataclass
class SongResponse(BaseResponse):
    """Represent Song Response Schema"""
    genre: str
    performer: str
    rating: int
    title: str
    year: int


@dataclass
class Playlist(BaseResponse):
    """Represent Playlist Schema"""
    user_name: str
    user_password: str
    playlist_name: str

@dataclass
class Voting(BaseResponse):
    """Represent Voting schema"""
    playlist_name: str
    song_title: str
    user_name: str
    user_password: str


@dataclass
class User(BaseResponse):
    """Represent User schema"""
    user_name: str
    user_password: str


@dataclass
class UserResponse(BaseResponse):
    """Represent User Response schema"""
    friends: list
    playlists: list
    user_name: str


@dataclass
class Friend(BaseResponse):
    """Represent Friend schema"""
    friend_name: str
    user_name: str
    user_password: str


@dataclass
class Password(BaseResponse):
    """Represent Password schema"""
    user_name: str
    user_new_password: str
    user_password: str
