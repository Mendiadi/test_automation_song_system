import pytest
import allure


from logic import db_schemas as schemas


@allure.epic("playlists api")
@pytest.mark.playlists
@pytest.mark.usefixtures("setup_teardown")
class TestPlaylists:

    # ADD_SONG TESTS

    @allure.story("as user im want to add songs to my playlists")
    def test_add_songs_to_playlist(self, set_up_playlist, set_up_song, playlists, users):
        playlist = set_up_playlist
        song = set_up_song
        assert playlists.add_song(song, playlist).data == song.song_title
        assert song.as_song_response() in users.get_playlist(playlist)

    @allure.story("as user im need to provide my password for add songs to my playlists")
    def test_add_songs_playlist_wrong_password(self, set_up_playlist, set_up_song, playlists, users):
        playlist = set_up_playlist
        song = set_up_song
        playlist.user_password = "wrongpass"
        assert playlists.add_song(song, playlist).error == 'either the user name or the password are wrong'

    @allure.story("for adding song to playlist first enter valid user_name")
    def test_add_songs_playlist_wrong_user(self, set_up_playlist, set_up_song, playlists, users):
        playlist = set_up_playlist
        song = set_up_song
        playlist.user_name = "wrongname"
        assert playlists.add_song(song, playlist).error == f'the user {playlist.user_name} does not exist'

    @allure.story("as user im dont want to add same song twice")
    def test_add_songs_playlists_twice(self, set_up_playlist, set_up_song, playlists, users):
        playlist = set_up_playlist
        song = set_up_song
        assert playlists.add_song(song, playlist).data == song.song_title
        assert playlists.add_song(song, playlist).error == f'the song {song.song_title} already exist in' \
                                                           ' the playlist or not in the songs collection'
        assert len(users.get_playlist(playlist)) == 1

    @allure.story("as user im want to add song to exists playlists")
    def test_add_songs_playlist_no_exists(self, set_up_user, set_up_song, playlists, users):
        user = set_up_user
        song = set_up_song
        playlist = schemas.Playlist.create_randomly(**user.as_json())
        playlist.as_add_song_schema(song.song_title)
        assert users.get_playlist(playlist).data is None
        assert playlists.add_song(song, playlist).error  # NOT SHOWING THE RIGHT ERROR MESSAGE

    @allure.story("as user im shouldnt be able to add not exists song to playlists")
    def test_add_songs_playlist_song_no_exists(self, playlists, set_up_playlist, users):
        song = schemas.Song.create_randomly()
        playlist = set_up_playlist
        assert playlists.add_song(song, playlist).error == f'the song {song.song_title} already exist in' \
                                                           ' the playlist or not in the songs collection'
        assert song.as_song_response() not in users.get_playlist(playlist)
