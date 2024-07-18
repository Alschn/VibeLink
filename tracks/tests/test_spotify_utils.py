from django.test import TestCase

from tracks.providers.spotify.utils import extract_spotify_track_id_from_url


class SpotifyRelatedUtilsTests(TestCase):

    def test_extract_track_id_from_url(self):
        track_id = '6jmTHeoWvBaSrwWttr8Xvu'
        url = f'https://open.spotify.com/track/{track_id}'
        extracted_track_id = extract_spotify_track_id_from_url(url)
        self.assertEqual(extracted_track_id, track_id)

    def test_extract_track_id_from_url_empty_match_group(self):
        url = 'https://open.spotify.com/track/'
        track_id = extract_spotify_track_id_from_url(url)
        self.assertEqual(track_id, None)

    def test_extract_track_id_from_url_no_match(self):
        url = 'https://open.spotify.com/tracks/1'
        track_id = extract_spotify_track_id_from_url(url)
        self.assertEqual(track_id, None)
