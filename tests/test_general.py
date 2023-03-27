import pytest
import allure

from logic import db_schemas as schemas


# just for general tests that not cover in APIS tests

@pytest.mark.general
@allure.epic("general tests")
@pytest.mark.usefixtures("setup_teardown")
class TestGeneral:

    def test_add_playlist_same_name_one_user(self, users, set_up_user):
        user = set_up_user

        assert users.add_playlist(schemas.Playlist(playlist_name="test1", **user.as_json())).data
        assert users.add_playlist(schemas.Playlist(playlist_name="test1", **user.as_json())).error
        # exp msg = "test1 already a playlist of Yhlnrj"

    def test_multiple_users_add_same_playlist_name(self, users):
        user1, user2 = schemas.User.create_randomly(user_name="adim111"), \
            schemas.User.create_randomly(user_name="adim333")
        users.add_user(user1)
        users.add_user(user2)
        assert users.add_playlist(schemas.Playlist(playlist_name="test", **user1.as_json())).data
        assert users.add_playlist(schemas.Playlist(playlist_name="test", **user2.as_json())).data

    @pytest.mark.xfail(reason="BUG: user can vote more then once per song")
    def test_user_can_upvote_once(self, songs, set_up_user, set_up_song, set_up_playlist):
        user = set_up_user
        playlist = set_up_playlist
        song = set_up_song
        vote = schemas.Voting(playlist.playlist_name, song.song_title, **user.as_json())
        assert songs.upvote(vote).data['rating'] == 1
        songs.upvote(vote)  # should not upvote
        assert songs.get_song(song.song_title).rating == 1

    @pytest.mark.xfail(reason="BUG user can downvote more then once per song")
    def test_user_can_downvote_once(self, songs, users, set_up_user, set_up_song, set_up_playlist):
        user = set_up_user
        user2 = schemas.User.create_randomly()
        users.add_user(user2)
        playlist = set_up_playlist
        song = set_up_song
        vote = schemas.Voting(playlist.playlist_name, song.song_title, **user2.as_json())
        vote2 = schemas.Voting(playlist.playlist_name, song.song_title, **user.as_json())
        assert songs.upvote(vote).data
        assert songs.upvote(vote2).data['rating'] == 2
        assert songs.downvote(vote).data
        songs.downvote(vote)  # should not downvote
        assert songs.get_song(song.song_title).rating == 1

    @allure.story("as user im want to delete songs from my playlist")
    def test_delete_songs(self):
        pytest.skip("not implement endpoint for delete")


    def test_rating_cant_less_then_zero(self, songs, set_up_song, set_up_playlist, set_up_user):
        user = set_up_user
        song = set_up_song
        playlist = set_up_playlist
        vote = schemas.Voting(playlist.playlist_name, song.song_title, **user.as_json())
        assert songs.get_song(song.song_title).rating == 0
        songs.downvote(vote)
        assert songs.get_song(song.song_title).rating == 0

    def test_add_multiple_playlists_for_user(self):
        ...
