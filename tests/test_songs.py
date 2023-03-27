import pytest
import allure

from logic import db_schemas as schemas
import utils


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

    @allure.story("need to add the song before get it")
    def test_get_song_no_exist(self, songs):
        assert songs.get_song("try to find me").error == 'this song does not exsist'

    @allure.story("must insert valid data for getting song")
    def test_get_song_invalid_data(self, songs):
        assert songs.get_song(None).error == 'Misssing parameter song_title'

    @allure.story("as user im want to upvote songs")
    def test_upvote_song(self, songs, set_up_song, set_up_user, set_up_playlist):
        song = set_up_song
        playlist = set_up_playlist
        user = set_up_user
        vote = schemas.Voting(playlist.playlist_name, song.song_title, **user.as_json())
        assert songs.get_song(song.song_title).rating == 0
        assert songs.upvote(vote).data['rating'] == 1
        assert songs.get_song(song.song_title).rating == 1

    @allure.story("need to insert valid data for upvoting songs")
    def test_upvote_song_invalid_data(self, songs):
        data = schemas.User.create_randomly()
        assert songs.upvote(data).error == "Misssing parameter song_title"

    @allure.story("users should not vote for no exists songs")
    def test_upvote_song_no_exists(self, songs, set_up_user, set_up_playlist):
        user = set_up_user
        playlist = set_up_playlist
        vote = schemas.Voting(playlist.playlist_name, "noexists", **user.as_json())
        assert songs.upvote(vote).error == "no such song in the songs collection"

    @allure.story("user should insert exists playlist for voting")
    @pytest.mark.xfail(reason="playlist not exists! why is it work? "
                              "why we need playlist for vote songs anyway?")
    def test_upvote_invalid_playlist(self, songs, set_up_song, set_up_user):
        user = set_up_user
        song = set_up_song
        vote = schemas.Voting("noexists", song.song_title, **user.as_json())
        assert songs.upvote(vote).error, "vote even playlist not exists"

    @allure.story("user should insert exists user for vote")
    def test_upvote_invalid_username(self, songs, set_up_song, set_up_playlist):
        playlist = set_up_playlist
        song = set_up_song
        vote = schemas.Voting.create_randomly(song_title=song.song_title,
                                              playlist_name=playlist.playlist_name)
        assert songs.upvote(vote).error == f"the user {vote.user_name} does not exist"

    @allure.story("user should enter correct password for voting")
    def test_upvote_invalid_password(self, songs, set_up_song, set_up_user, set_up_playlist):
        user = set_up_user
        song = set_up_song
        playlist = set_up_playlist
        vote = schemas.Voting(playlist.playlist_name, song.song_title,
                              user.user_name, "badpassword!!")
        assert songs.upvote(vote).error == "either the user name or the password are wrong"

    @allure.story("as user im want to downvote songs")
    def test_downvote_song(self, songs, set_up_song, set_up_user, set_up_playlist):
        song = set_up_song
        playlist = set_up_playlist
        user = set_up_user
        vote = schemas.Voting(playlist.playlist_name, song.song_title, **user.as_json())
        assert songs.get_song(song.song_title).rating == 0
        assert songs.upvote(vote).data['rating'] == 1
        assert songs.get_song(song.song_title).rating == 1
        assert songs.downvote(vote).data['rating'] == 0
        assert songs.get_song(song.song_title).rating == 0

    @allure.story("need to insert valid data for downvoting songs")
    def test_downvote_song_invalid_data(self, songs):
        data = schemas.User.create_randomly()
        assert songs.downvote(data).error == "Misssing parameter song_title"

    @allure.story("users should not downvote for no exists songs")
    def test_downvote_song_no_exists(self, songs, set_up_user, set_up_playlist):
        user = set_up_user
        playlist = set_up_playlist
        vote = schemas.Voting(playlist.playlist_name, "noexists", **user.as_json())
        assert songs.downvote(vote).error == "no such song in the songs collection"

    @allure.story("user should insert exists playlist for downvoting")
    @pytest.mark.xfail(reason="playlist not exists! why is it work? "
                              "why we need playlist for vote songs anyway?")
    def test_downvote_invalid_playlist(self, songs, set_up_song, set_up_user):
        user = set_up_user
        song = set_up_song
        vote = schemas.Voting("noexists", song.song_title, **user.as_json())
        assert songs.downvote(vote).error, "vote even playlist not exists"

    @allure.story("user should insert exists user for downvote")
    def test_downvote_invalid_username(self, songs, set_up_song, set_up_playlist):
        playlist = set_up_playlist
        song = set_up_song
        vote = schemas.Voting.create_randomly(song_title=song.song_title,
                                              playlist_name=playlist.playlist_name)
        assert songs.downvote(vote).error == f"the user {vote.user_name} does not exist"

    @allure.story("user should enter correct password for downvoting")
    def test_downvote_invalid_password(self, songs, set_up_song, set_up_user, set_up_playlist):
        user = set_up_user
        song = set_up_song
        playlist = set_up_playlist
        vote = schemas.Voting(playlist.playlist_name, song.song_title,
                              user.user_name, "badpassword!!")
        assert songs.downvote(vote).error == "either the user name or the password are wrong"

    @allure.story("as user im should find songs by ranks")
    @pytest.mark.parametrize("rate", [1, 2, 0])
    def test_ranked_songs_equal(self, setup_songs, songs, rate):
        for s in songs.ranked_songs("eq", rate):
            assert songs.get_song(s).rating == rate

    @allure.story("as user im should find songs by ranks")
    @pytest.mark.parametrize("rate", [1, 2, 0])
    def test_ranked_songs_greater(self, setup_songs, songs, rate):
        for song_title in songs.ranked_songs("greater", rate):
            if song_title:
                assert songs.get_song(song_title).rating > rate

    @allure.story("as user im should find songs by ranks")
    @pytest.mark.parametrize("rate", [1, 2, 0])
    def test_ranked_songs_less(self, songs, setup_songs, rate):
        for song_title in songs.ranked_songs("less", rate):
            if song_title:
                assert songs.get_song(song_title).rating < rate

    @allure.story("as user im should find songs by with only valid data")
    @pytest.mark.xfail(reason="BUG : server returns 500 (server error) instead of "
                              "informative error message...dev team should fix that")
    def test_ranked_songs_invalid_data(self, songs):
        assert songs.ranked_songs("invalid", 100).error
        assert songs.ranked_songs("less", "error").error
