from django.test import TestCase

from tracks.providers.youtube.utils import extract_youtube_video_id_from_url


class YoutubeRelatedUtilsTests(TestCase):

    def test_extract_track_id_from_url(self):
        video_id = 'kJQP7kiw5Fk'
        url = f'https://www.youtube.com/watch?v={video_id}'
        extracted_video_id = extract_youtube_video_id_from_url(url)
        self.assertEqual(extracted_video_id, video_id)

    def test_extract_track_id_from_url_empty_match_group(self):
        url = f'https://www.youtube.com/watch?v='
        video_id = extract_youtube_video_id_from_url(url)
        self.assertEqual(video_id, None)

    def test_extract_track_id_from_url_no_match(self):
        url = f'https://www.youtube.com/watch?video='
        video_id = extract_youtube_video_id_from_url(url)
        self.assertEqual(video_id, None)
