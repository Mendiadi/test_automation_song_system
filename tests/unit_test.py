import datetime

import allure
import pytest



import utils
import logic




@allure.epic("unit")
@pytest.mark.unit
class TestUtils:

    def test_excepted_msg(self):
        param = "test"
        msg_func = utils.expected_msg("this is my %s msg")
        assert msg_func(param) == "this is my test msg"

    def test_build_str(self):
        sample_str2 = "hello"
        sample_list_str = ["hi", "im", "eat", "banana"]
        assert utils.build_str(lambda s: " ".join(s), 2, sample_list_str, space=True) == \
               "hi im eat banana hi im eat banana "
        assert utils.build_str(lambda s: s + " ", 3, sample_str2) == \
               "hello hello hello "
        assert utils.build_str(lambda i, s: str(range(i, s)), 4, 10, 20, space=True) == \
               "range(10, 20) range(10, 20) range(10, 20) range(10, 20) "

    def test_random_name(self):
        for i in range(1, 25):
            name = utils.random_name(i)
            list_of_bool = [l.isalpha() and l.islower() if i > 0 else l.isupper() for i, l in enumerate(name)]
            assert len(name) == i
            assert all(list_of_bool)

    def test_random_year(self):
        for _ in range(25):
            year = utils.random_year()
            assert type(year) == int
            assert year in range(1900, 2023)

    def test_random_title(self):
        for i in range(1, 25):
            words = utils.random_title(i)
            assert len(words.split()) == i

    def test_random_password(self):
        def helper(s):
            return s.isalpha() or s.isdigit()

        for i in range(1, 25):
            password = utils.random_pass(i)
            assert len(password) == i
            assert all([helper(p) for p in password])

    def test_my_origin(self):
        def foobar():
            return foo()

        def foo():
            return utils.my_origin(3)

        def bar():
            return utils.my_origin(1)

        str = utils.my_origin(0)
        assert f"help_utils.py::def my_origin(...)::line " in str
        assert f"unit_test.py::def test_my_origin(...)::line " in foobar()
        assert f"unit_test.py::def bar(...)::line " in bar()

    def test_get_generic_random_schema(self):
        attrs_ = [("name", str), ("age", str), ("food", str)]
        test_data = dict(name="test", age="test", food="test")
        data = utils.get_generic_random_schema(attrs_, {}, dict)
        test_data2 = dict(name="test", age="test", food="test")
        data2 = utils.get_generic_random_schema(attrs_, {"water": "hi"}, dict)
        test_data2["water"] = "hi"
        assert data.keys() == test_data.keys()
        assert data2.keys() == test_data2.keys()
        assert data2.get("water") == test_data2.get("water")

@allure.epic("unit")
@pytest.mark.unit
class TestLogger:
    _time_format = '%Y-%m-%d %H:%M:%S'
    _time_format2 = '%Y/%m/%d %H:%M:%S'
    _format = '%(asctime)-4s [%(levelname)-4s] %(message)s'
    _format2 = '[%(levelname)-4s] %(asctime)-4s %(message)s'

    @staticmethod
    def t_format(f: str) -> str:
        return datetime.datetime.today().strftime(f)

    @pytest.mark.parametrize("timef,format,lvl,i,excepted",
                             [(_time_format, _format, "info", 0, f"{t_format(_time_format)} [INFO] this is test!"),
                              (_time_format2, _format2, "error", 1, f"[ERROR] {t_format(_time_format2)} this is test!"),
                              (_time_format, _format, "none", 3, f"{t_format(_time_format)} [INFO] this is test!")])
    def test_log_to_file(self, timef, format, lvl, i, excepted):

        utils.unit_logger.setup_file("test_logs_unit.txt")
        utils.unit_logger.set_formatter(format, timef)
        utils.unit_logger.log("this is", "test!", level=lvl)
        with open("logs.txt", "r") as f:
            lines = f.readlines()
            assert excepted == lines[i].replace("\n", "")


@allure.epic("unit")
@pytest.mark.unit
class TestInfra:
    def test_send(self, init_session):
        r = init_session.send("http://google.com", "GET")
        assert r
        assert r.request.method == "GET"

    def test_send_invalid(self, init_session):
        assert init_session.send("http://127.1.1.0:1000/", "PUT", json={"test": "put"}) is None

@allure.epic("unit")
@pytest.mark.unit
class TestSchemas:
    def test_create_from_response(self):
        class foo:
            def __init__(self, d):
                self.data = d

            def json(self):
                return self.data

        u = {"data": {"user_name": "asdfasf", "user_password": "safasf"}}
        u1 = {"error": "asfdasfasfasf"}
        s = logic.BaseResponse.create_from_response(foo({"sm": "lo", "data": {"name": "invalid", "no": "pass"}}))
        s1 = logic.User.create_from_response(foo(u))
        s2 = logic.Password.create_from_response(foo(u1))
        assert s.as_json() == {"sm": "lo", "data": {"name": "invalid", "no": "pass"}} and s.sm == "lo"
        assert s1.as_json() == u['data'] and s1.user_name == u['data']['user_name']
        assert s2.as_json() == u1 and s2.error == "asfdasfasfasf"

    def test_equal_between_schemas(self):
        s = logic.BaseResponse(name="adi", aim="good", level="high")
        s1 = logic.BaseResponse(name="adi", aim="good", level="high")
        assert s == s1
        s1 = logic.BaseResponse(aim="good", dor="yes")
        assert s1.aim == "good" and s != s1
        s1 = logic.BaseResponse(name="adi", aim="good", level="low")
        assert s1 != s
        s2 = logic.User("adi", "adi")
        s3 = logic.User("adi", "adi")
        assert s2 == s3 and s2 != logic.User("adi", "adi1")
        assert logic.User("adi", "adi") != logic.BaseResponse(user_name="adi", user_password="adi")
