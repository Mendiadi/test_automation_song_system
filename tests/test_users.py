import pytest

import utils

from schemas import db_schemas

user_exists_err_msg = lambda u: f"user with name {u} already exists."
user_not_exists_err_msg = lambda u: f"user {u} does not exist"
user_miss_param = lambda p: f"Misssing parameter {p}"


@pytest.mark.usefixtures("setup_teardown")
class TestUsers:
    def test_add_user(self,users):
        new_user = db_schemas.User.create_randomly()
        response = users.add_user(new_user)
        assert response.messgae == "OK"
        assert response.data == new_user.user_name
        get_the_user = users.get_user(new_user.user_name)
        assert get_the_user.user_name == new_user.user_name


    def test_add_user_already_exists(self,users):
        new_user = db_schemas.User.create_randomly(user_name="adim333")
        assert users.add_user(new_user).data =="adim333"
        assert users.get_user("adim333").user_name == "adim333"
        assert users.add_user(new_user).error == user_exists_err_msg(new_user.user_name)


    @pytest.mark.parametrize("username,password,msg,param", [
        ("username11", None,
         user_not_exists_err_msg("username11"), "user_password")
        , (None, "password!!",
           user_miss_param("user_name"), "user_name")])

    def test_add_user_invalid_data(self,users, username, password, msg, param):
        u = db_schemas.User(username, password)
        assert users.add_user(u).error == user_miss_param(param)
        assert users.get_user(username).error == msg
