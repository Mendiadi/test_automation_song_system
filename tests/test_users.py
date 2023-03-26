import pytest
import allure

from logic import db_schemas as schemas
from utils import expected_msg

# DEFINE ERROR MESSAGES

exists_e_msg = expected_msg("user with name %s already exists.")
not_exists_e_msg = expected_msg("user %s does not exist")
not_exists_e_msg_2 = expected_msg("the user %s does not exist")
user_miss_param = expected_msg("Misssing parameter %s")
pass_or_name_wrong_e_msg = "either the user name or the password are wrong"


@allure.epic("users api")
@pytest.mark.users
@pytest.mark.usefixtures("setup_teardown")
class TestUsers:

    # ADD_USER TESTS

    @allure.story("a client need to add user")
    def test_add_user(self, users):
        new_user = schemas.User.create_randomly()
        assert users.add_user(new_user).data == new_user.user_name, "adding user function failed"
        get_the_user = users.get_user(new_user.user_name)
        assert get_the_user.user_name == new_user.user_name, "user has not added as excepted"

    @allure.story("a client cant add exists usernames")
    def test_add_user_already_exists(self, users):
        user = schemas.User.create_randomly(user_name="adim333")
        assert users.add_user(user).data == "adim333", "adding user function failed"
        assert users.get_user("adim333").user_name == "adim333", "user has not added as excepted"
        assert users.add_user(user).error == exists_e_msg(user.user_name), "exists user shouldn't be added"

    @allure.story("a client need to insert username and password")
    @pytest.mark.parametrize("username,password,msg,param", [
        ("username11", None,
         not_exists_e_msg("username11"), "user_password")
        , (None, "password!!",
           user_miss_param("user_name"), "user_name")])
    def test_add_user_invalid_data(self, users, username, password, msg, param):
        u = schemas.User(username, password)
        assert users.add_user(u).error == user_miss_param(param), f"error massage not helping"
        assert users.get_user(username).error == msg, f"user added without {param}"

    # GET_USER TESTS

    @allure.story("im want to be able to see users")
    def test_get_user(self, users):
        user = schemas.User.create_randomly()
        assert users.add_user(user).data == user.user_name, "adding user function failed"
        assert users.get_user(user.user_name).user_name == user.user_name, "user has not added as excepted"

    @allure.story("when im search not exists user")
    def test_get_user_not_exists(self, users):
        assert users.get_user("myuser222").error == not_exists_e_msg("myuser222") \
            , "message not shows as excepted"

    # CHANGE_PASSWORD TESTS

    @allure.story("as user im want to change password")
    def test_change_password(self, users, set_up_user):
        user = set_up_user
        password = schemas.Password(user.user_name, "newpass", user.user_password)
        assert users.change_password(password).user_name == user.user_name, "password didnt change"
        playlist = schemas.Playlist(user.user_name, password.user_new_password, "mysongs")
        assert users.get_playlist(playlist).message == "OK"

    @allure.story("for change password need to provide old password")
    def test_change_password_invalid_user_password(self, users, set_up_user):
        user = set_up_user
        password = schemas.Password(user.user_name, "newpass", "wrongpass")
        assert users.change_password(password).error, "error not provided"

    @allure.story("dont change password without new password")
    def test_change_password_invalid_new_password(self, users, set_up_user):
        user = set_up_user
        password = schemas.Password(user.user_name, None, "wrongpass")
        assert users.change_password(password).error, "error not provided"

    @allure.story("provide a valid user to change password")
    def test_change_password_invalid_username(self, users):
        password = schemas.Password("notexists", "newpass", "wrongpass")
        assert users.change_password(password).error, "error not provided"

    @allure.story("provide a valid parameters to change password")
    def test_change_password_invalid_params(self, users):
        param = schemas.BaseResponse(user="test", wrong_param="wrong")
        assert users.change_password(param).error == user_miss_param("user_name")

    # ADD_PLAYLIST TESTS

    @allure.story("as user im want to add playlist")
    def test_add_playlist(self, users, set_up_user):
        user = set_up_user
        user_playlist = users.get_user(user.user_name).playlists
        assert user_playlist == []
        playlist = schemas.Playlist.create_randomly(user_name=user.user_name, user_password=user.user_password)
        assert users.add_playlist(playlist).data == playlist.playlist_name
        assert playlist.playlist_name in users.get_user(user.user_name).playlists
        assert users.get_playlist(playlist).message == "OK"

    @allure.story("playlists must be created by valid users")
    def test_add_playlist_not_exists_user(self, users):
        playlist = schemas.Playlist.create_randomly()
        assert users.add_playlist(playlist).error == not_exists_e_msg_2(playlist.user_name)
        assert users.get_playlist(playlist).error == not_exists_e_msg_2(playlist.user_name)

    @allure.story("must provide valid password for adding playlist")
    def test_add_playlist_wrong_password(self, users, set_up_user):
        user = set_up_user
        playlist = schemas.Playlist.create_randomly(user_name=user.user_name)
        assert users.add_playlist(playlist).error == pass_or_name_wrong_e_msg
        assert playlist.playlist_name not in users.get_user(user.user_name).playlists
        assert users.get_playlist(playlist).error == pass_or_name_wrong_e_msg

    @allure.story("for adding playlists need to passing correct params")
    def test_add_playlist_with_wrong_params(self, users):
        f = schemas.Friend.create_randomly()
        assert users.add_playlist(f).error == user_miss_param("playlist_name")

    # GET_PLAYLIST TESTS

    @allure.story("as user im should able to get playlists")
    # @pytest.xfail(reason="BUG - playlist name not provided")
    def test_get_playlist(self, users, set_up_user):
        user = set_up_user
        playlist = schemas.Playlist.create_randomly(user_name=user.user_name, user_password=user.user_password)
        assert users.add_playlist(playlist).message == "OK"
        get_playlist = users.get_playlist(playlist)
        assert get_playlist.message == "OK"
        assert get_playlist.data == [], "playlist not provided"

    @allure.story("must provide valid data for getting playlist")
    def test_get_playlist_wrong_data(self, users):
        wrong_data = schemas.Password.create_randomly()
        assert users.get_playlist(wrong_data).error == user_miss_param("playlist_name")

    @allure.story("for get playlist user must provide exists playlist")
    def test_get_playlist_no_exists(self, users, set_up_user):
        user = set_up_user
        playlist = schemas.Playlist.create_randomly(user_name=user.user_name, user_password=user.user_password)
        assert users.add_playlist(playlist).message == "OK"
        playlist.playlist_name = "moshe hits 2020"
        assert users.get_playlist(playlist).data is None

    # ADD_FRIEND TESTS

    @allure.story("as a user im want to add users friends")
    def test_add_friend(self, users, set_up_user):
        user = set_up_user
        user_friend = schemas.User.create_randomly()
        friend = schemas.Friend(user_friend.user_name, user.user_name, user.user_password)
        assert users.add_friend(friend).data == friend.friend_name
        assert friend.friend_name in users.get_user(user.user_name).friends

    @allure.story("as user im need provide my password for adding friends")
    def test_add_friend_wrong_password(self, users, set_up_user):
        user = set_up_user
        user_friend = schemas.User.create_randomly()
        assert users.add_user(user_friend).message == "OK"
        friend = schemas.Friend.create_randomly(user_name=user.user_name, friend_name=user_friend.user_name)
        assert users.add_friend(friend).error == pass_or_name_wrong_e_msg
        assert friend.friend_name not in users.get_user(user.user_name).friends

    @allure.story("must provide valid username for add friend")
    def test_add_friend_wrong_user(self, users):
        user_friend = schemas.User.create_randomly()
        assert users.add_user(user_friend).message == "OK"
        friend = schemas.Friend.create_randomly(friend_name=user_friend.user_name)
        assert users.add_friend(friend).error == not_exists_e_msg_2(friend.user_name)

    @allure.story("must provide valid user friend for add friend")
    @pytest.mark.xfail(reason="BUG- Error message are wrong")
    def test_add_friend_no_friend_user(self, users, set_up_user):
        user = set_up_user
        friend = schemas.Friend("notexists", user.user_name, user.user_password)
        assert users.get_user(friend.friend_name).error == not_exists_e_msg(friend.friend_name)
        assert friend.friend_name not in users.get_user(user.user_name).friends, "friend added even not exists"
        assert users.add_friend(friend).error == not_exists_e_msg_2(friend.friend_name), \
            "error message not shows up like excepted"

    @allure.story("as user im dont want to add friend twice")
    def test_add_friend_twice(self, users, set_up_user):
        user = set_up_user
        friend = schemas.Friend.create_randomly(**user.as_json())
        users.add_friend(friend)
        assert users.add_friend(friend).error == f'{friend.friend_name} already a friend of {user.user_name}'
