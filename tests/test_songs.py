import pytest
import allure

from logic import db_schemas as schemas


@allure.epic("songs api")
@pytest.mark.songs
@pytest.mark.usefixtures("setup_teardown")
class TestSongs:

    # ADD_SONG TESTS

    @allure.story("as a user im should add songs to system")
    def test_add_song(self, songs):
        song = schemas.Song.create_randomly()
        assert songs.add_song(song).message
        get_song = songs.get_song(song.song_title)
        assert get_song == song.as_song_response()
        assert get_song.rating == 0

    @allure.story("as user im need to add song with valid data")
    def test_add_song_invalid_data(self, songs):
        song = schemas.BaseSchema(location="test", evn="system32")
        assert songs.add_song(song).error == 'Misssing parameter song_title'

    @allure.story("as user im want year only in valid format")
    @pytest.mark.xfail(reason="song created with not valid year")
    def test_add_song_invalid_data_type(self, songs):
        song = schemas.Song.create_randomly(song_year={"invalid": "type"})
        assert not songs.add_song(song).error
        year = songs.get_song(song.song_title).year
        assert year != {"invalid": "type"}, "song added with year that not valid"

    # GET_SONG TESTS
    @allure.story("as user im should get songs from the system")
    def test_get_song(self, songs):
        song = schemas.Song.create_randomly(song_title="good sh1t")
        assert songs.add_song(song).data
        assert songs.get_song("good sh1t") == song.as_song_response()

    def test_get_song_no_exist(self, songs):
        assert songs.get_song("try to find me").error == 'this song does not exsist'

    def test_get_song_invalid_data(self, songs):
        assert songs.get_song(None).error == 'Misssing parameter song_title'
