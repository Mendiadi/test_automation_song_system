import pytest
import allure

from logic import db_schemas as schemas


@pytest.mark.admin
@allure.epic("admin tests")
class TestAdmin:

    def test_delete_all_users(self, admin, set_up_user, users):
        user = set_up_user
        admin.delete_all_users()
        assert users.get_user(user.user_name).error

    def test_delete_all_songs(self, admin, set_up_song, songs):
        song = set_up_song
        admin.delete_all_song()
        assert songs.get_song(song.song_title).error

    @pytest.mark.xfail(reason="Error 500 from server...")
    def test_set_songs(self, admin, songs):
        songs_list = [schemas.Song.create_randomly() for _ in range(3)]
        song_list_as_titles = [song.song_title for song in songs_list]
        assert not admin.set_songs(songs_list).error
        for song in song_list_as_titles:
            assert songs.get_song(song).title == song

    @pytest.mark.xfail(reason="Error 500 from server...")
    def test_set_user(self, admin, users):
        user_list = [schemas.User.create_randomly() for _ in range(3)]
        user_names_list = [user.user_name for user in user_list]
        assert not admin.set_users(user_list).error
        for user in user_names_list:
            assert users.get_user(user).title == user
