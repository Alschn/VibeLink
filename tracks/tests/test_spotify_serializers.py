from django.test import TestCase

from tracks.providers.spotify.models import SpotifyTrack
from tracks.providers.spotify.serializers import SpotifyTrackSerializer


class SpotifySerializersTests(TestCase):

    def test_track_serializer(self):
        sample_spotify_data = {
            'album':
                {
                    'album_type': 'album',
                    'artists': [
                        {
                            'external_urls': {'spotify': 'https://open.spotify.com/artist/02kJSzxNuaWGqwubyUba0Z'},
                            'href': 'https://api.spotify.com/v1/artists/02kJSzxNuaWGqwubyUba0Z',
                            'id': '02kJSzxNuaWGqwubyUba0Z', 'name': 'G-Eazy', 'type': 'artist',
                            'uri': 'spotify:artist:02kJSzxNuaWGqwubyUba0Z'
                        }
                    ],
                    'available_markets': ['US'],
                    'external_urls': {'spotify': 'https://open.spotify.com/album/6wDc63NhKy2PyXdbhkRmrl'},
                    'href': 'https://api.spotify.com/v1/albums/6wDc63NhKy2PyXdbhkRmrl',
                    'id': '6wDc63NhKy2PyXdbhkRmrl',
                    'images': [
                        {
                            'height': 640,
                            'url': 'https://i.scdn.co/image/ab67616d0000b273bdfe4efd674482cf5ac88c99',
                            'width': 640
                        },
                        {
                            'height': 300,
                            'url': 'https://i.scdn.co/image/ab67616d00001e02bdfe4efd674482cf5ac88c99',
                            'width': 300
                        },
                        {
                            'height': 64,
                            'url': 'https://i.scdn.co/image/ab67616d00004851bdfe4efd674482cf5ac88c99',
                            'width': 64
                        }
                    ],
                    'name': 'These Things Happen',
                    'release_date': '2014-06-20',
                    'release_date_precision': 'day',
                    'total_tracks': 16,
                    'type': 'album',
                    'uri': 'spotify:album:6wDc63NhKy2PyXdbhkRmrl'
                },
            'artists': [
                {
                    'external_urls': {'spotify': 'https://open.spotify.com/artist/02kJSzxNuaWGqwubyUba0Z'},
                    'href': 'https://api.spotify.com/v1/artists/02kJSzxNuaWGqwubyUba0Z',
                    'id': '02kJSzxNuaWGqwubyUba0Z',
                    'name': 'G-Eazy',
                    'type': 'artist',
                    'uri': 'spotify:artist:02kJSzxNuaWGqwubyUba0Z'
                },
                {
                    'external_urls': {'spotify': 'https://open.spotify.com/artist/7rVA45AaxEEetdqc9NngiJ'},
                    'href': 'https://api.spotify.com/v1/artists/7rVA45AaxEEetdqc9NngiJ',
                    'id': '7rVA45AaxEEetdqc9NngiJ',
                    'name': 'Remo',
                    'type': 'artist',
                    'uri': 'spotify:artist:7rVA45AaxEEetdqc9NngiJ'
                }
            ],
            'available_markets': ['US'],
            'disc_number': 1,
            'duration_ms': 236480,
            'explicit': True,
            'external_ids': {'isrc': 'USRC11400730'},
            'external_urls': {'spotify': 'https://open.spotify.com/track/6jmTHeoWvBaSrwWttr8Xvu'},
            'href': 'https://api.spotify.com/v1/tracks/6jmTHeoWvBaSrwWttr8Xvu',
            'id': '6jmTHeoWvBaSrwWttr8Xvu',
            'is_local': False,
            'name': 'I Mean It (feat. Remo)',
            'popularity': 71,
            'preview_url': 'https://p.scdn.co/mp3-preview/65fc6e30e41d1253880731912a1e3d0f0033e3ad?cid=1e10bbb250eb430e9860b171f1cf8c10',
            'track_number': 3,
            'type': 'track',
            'uri': 'spotify:track:6jmTHeoWvBaSrwWttr8Xvu'
        }

        serializer = SpotifyTrackSerializer(data=sample_spotify_data)
        serializer.is_valid(raise_exception=True)
        spotify_track = serializer.save()
        serialized_data = serializer.data
        expected_data = {
            'id': '6jmTHeoWvBaSrwWttr8Xvu',
            'href': 'https://api.spotify.com/v1/tracks/6jmTHeoWvBaSrwWttr8Xvu',
            'name': 'I Mean It (feat. Remo)',
            'uri': 'spotify:track:6jmTHeoWvBaSrwWttr8Xvu',
            'duration_ms': 236480,
            'explicit': True,
            'preview_url': 'https://p.scdn.co/mp3-preview/65fc6e30e41d1253880731912a1e3d0f0033e3ad?cid=1e10bbb250eb430e9860b171f1cf8c10',
            'external_ids': {'isrc': 'USRC11400730'},
            'external_urls': {'spotify': 'https://open.spotify.com/track/6jmTHeoWvBaSrwWttr8Xvu'},
            'album': {
                'id': '6wDc63NhKy2PyXdbhkRmrl',
                'name': 'These Things Happen',
                'uri': 'spotify:album:6wDc63NhKy2PyXdbhkRmrl',
                'album_type': 'album',
                'total_tracks': 16,
                'href': 'https://api.spotify.com/v1/albums/6wDc63NhKy2PyXdbhkRmrl',
                'external_urls': {'spotify': 'https://open.spotify.com/album/6wDc63NhKy2PyXdbhkRmrl'},
                'release_date': '2014-06-20',
                'images': [
                    {
                        'height': 640,
                        'url': 'https://i.scdn.co/image/ab67616d0000b273bdfe4efd674482cf5ac88c99',
                        'width': 640
                    },
                    {
                        'height': 300,
                        'url': 'https://i.scdn.co/image/ab67616d00001e02bdfe4efd674482cf5ac88c99',
                        'width': 300
                    },
                    {
                        'height': 64,
                        'url': 'https://i.scdn.co/image/ab67616d00004851bdfe4efd674482cf5ac88c99',
                        'width': 64
                    }
                ],
                'artists': [
                    {
                        'id': '02kJSzxNuaWGqwubyUba0Z',
                        'name': 'G-Eazy',
                        'uri': 'spotify:artist:02kJSzxNuaWGqwubyUba0Z',
                        'href': 'https://api.spotify.com/v1/artists/02kJSzxNuaWGqwubyUba0Z',
                        'external_urls': {'spotify': 'https://open.spotify.com/artist/02kJSzxNuaWGqwubyUba0Z'},
                    }
                ]
            },
            'artists': [
                {
                    'id': '02kJSzxNuaWGqwubyUba0Z',
                    'name': 'G-Eazy',
                    'uri': 'spotify:artist:02kJSzxNuaWGqwubyUba0Z',
                    'href': 'https://api.spotify.com/v1/artists/02kJSzxNuaWGqwubyUba0Z',
                    'external_urls': {'spotify': 'https://open.spotify.com/artist/02kJSzxNuaWGqwubyUba0Z'}
                },
                {
                    'id': '7rVA45AaxEEetdqc9NngiJ',
                    'name': 'Remo',
                    'uri': 'spotify:artist:7rVA45AaxEEetdqc9NngiJ',
                    'href': 'https://api.spotify.com/v1/artists/7rVA45AaxEEetdqc9NngiJ',
                    'external_urls': {'spotify': 'https://open.spotify.com/artist/7rVA45AaxEEetdqc9NngiJ'},
                }
            ],
        }

        self.assertEqual(serialized_data, expected_data)
        self.assertTrue(isinstance(spotify_track, SpotifyTrack))
