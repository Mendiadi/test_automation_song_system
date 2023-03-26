import pytest
import allure

from logic import db_schemas as schemas
from utils import expected_msg

# DEFINE ERROR MESSAGES

exists_e_msg = expected_msg("user with name %s already exists.")
not_exists_e_msg = expected_msg("user %s does not exist")
user_miss_param = expected_msg("Misssing parameter %s")


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
    def test_change_password(self, users,set_up_user):
        user = set_up_user
        password = schemas.Password(user.user_name, "newpass", user.user_password)
        assert users.change_password(password).user_name == user.user_name, "password didnt change"
        playlist = schemas.Playlist(user.user_name,password.user_new_password,"mysongs")
        assert users.get_playlist(playlist).message == "OK"

    @allure.story("for change password need to provide old password")
    def test_change_password_invalid_user_password(self, users,set_up_user):
        user = set_up_user
        password = schemas.Password(user.user_name, "newpass", "wrongpass")
        assert users.change_password(password).error,  "error not provided"

    @allure.story("dont change password without new password")
    def test_change_password_invalid_new_password(self, users,set_up_user):
        user = set_up_user
        password = schemas.Password(user.user_name, None, "wrongpass")
        assert users.change_password(password).error, "error not provided"

    @allure.story("provide a valid user to change password")
    def test_change_password_invalid_username(self, users):
        password = schemas.Password("notexists", "newpass", "wrongpass")
        assert users.change_password(password).error, "error not provided"

    # ADD_PLAYLIST TESTS

    @allure.story("as user im want to add playlist")
    def test_add_playlist(self,users,set_up_user):
        user =  set_up_user
        user_playlist = users.get_user(user.user_name).playlists
        assert user_playlist == []
        playlist= schemas.Playlist.create_randomly(user_name=user.user_name,user_password=user.user_password)
        assert users.add_playlist(playlist).data == playlist.playlist_name
        assert playlist.playlist_name in users.get_user(user.user_name).playlists
        assert users.get_playlist(playlist)


    @allure.story("as a user im want to add users friends")
    def test_add_friend(self,users,set_up_user):
        user = set_up_user
        user_friend = schemas.User.create_randomly()
        friend = schemas.Friend(user_friend.user_name,user.user_name,user.user_password)
        assert users.add_friend(friend).data == friend.friend_name
        assert friend.friend_name in users.get_user(user.user_name).friends

