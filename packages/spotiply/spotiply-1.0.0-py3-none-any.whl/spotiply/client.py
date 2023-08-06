__all__ = [
    "Spotify"
]

import json
from typing import Any
import requests
from urllib.parse import urlencode
from spotiply.exceptions import SpotifyException


class Spotify():

    def __init__(self, access_token: str):
        self._access_token = access_token
        self._baseUrl = 'https://api.spotify.com/v1/'

    @property
    def access_token(self):
        return self._access_token

    def search_header(self):
        return {
            "Authorization": f"Bearer {self.access_token}"
        }

    def _APIBaseUrl(self, endpoint: str, query_params: str = None):
        url = f'{self._baseUrl}{endpoint}'
        if query_params:
            url += f'?{query_params}'
        return url

    # Helper
    def _requests(self, action: Any,
                  endpoint: str,
                  query_params: dict[Any, Any] = None,
                  data: dict[Any, Any] = None):
        """requests module helper for web requests

        Args:
            action (str): The desired action e.g `requests.get`,\
             `requests.post`
            endpoint (str): The Spotify API Endpoint
            query_params (str, optional): query_parameters. Defaults to None.
            data (str, optional): Request Body. Defaults to None.

        Returns:
            method: A method
        """
        qParams = urlencode(query_params) if query_params else None
        bodyParams = json.dumps(data) if data else None

        url = self._APIBaseUrl(endpoint, qParams)
        return action(url,
                      headers=self.search_header(),
                      data=bodyParams)

    def _baseSearch(self, _id, return_type):
        endpoint = f"https://api.spotify.com/v1/{return_type}/{_id}"
        headers = self.search_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code != 200:
            return {}
        else:
            return r.json()

    # Search tracks by ID
    def track(self, track_id):
        """Get a single track

        Args:
         - track_id (str): the track ID

        Returns:
         - dict : returns a single track given the album’s ID
        """
        return self._baseSearch(_id=track_id, return_type="tracks")

    def tracks(self, track_ids: list[str]):
        """
        Get several tracks

        =========

        Args:

         - track_id (list, required): A list of Spotify track IDs. Maximum:50.

        Returns:
         - dict: Returned json formatted result.
        """
        track_id = ",".join(track_ids)

        return self._baseSearch(_id=f"?ids={track_id}&market=PH",
                                return_type="tracks")

    def audio_features_for_track(self, track_id):
        """Get Audio Features for a track

        Args:
            track_id (str): the track ID

        Returns:
            dict: returns a track features
        """
        return self._baseSearch(_id=f"?ids={track_id}&market=PH",
                                return_type="audio-features")

    def audio_features_for_tracks(self, track_id):
        """
        Get Audio Features for Several Tracks

        Args:
            track_id (list): Required. A list of Spotify track IDs

        Returns:
            dict: returns a list of several track features.
        """
        track_id = ",".join(track_id)

        return self._baseSearch(_id=f"?ids={track_id}&market=PH",
                                return_type="audio-features")

    def audio_analysis_for_track(self, track_id):
        """
        Get Audio Analysis for a Track

        Args:

         - track_id (str): Required. A Spotify track ID

        Returns:
            dict: returns a audio analysis for a track

        """
        return self._baseSearch(_id=track_id, return_type="audio-analysis")

    # Search albums by ID
    def album(self, album_id: str):
        return self._baseSearch(_id=album_id, return_type="albums")

    def albums(self, album_id: str):
        album_id = ",".join(album_id)
        return self._baseSearch(_id=f"?ids={album_id}&market=PH",
                                return_type="albums")

    def album_tracks(self, album_id: str, limit=20):
        """Get an Album track

        Args:
            album_id (str): Album ID
            limit (int, optional): How many results you wish to return to you.
            Defaults to 20.

        Returns:
            dict: Album tracks details
        """
        query_params = f"{album_id}/tracks?market=PH&limit={limit}"
        return self._baseSearch(_id=query_params,
                                return_type="albums")

    # Search artists by ID
    def artist(self, artist_id: str):
        return self._baseSearch(_id=artist_id, return_type="artists")

    def artists(self, artist_id: str):
        artist_id = ",".join(artist_id)
        return self._baseSearch(_id=f"?ids={artist_id}&market=PH",
                                return_type="artists")

    def artist_albums(self,
                      artist_id: str,
                      limit: int = 20,
                      include_groups: str = "album",
                      country: str = "PH",
                      offset: int = 0):
        query_params = urlencode({
            "include_groups": include_groups,
            "country": country,
            "limit": limit,
            "offset": offset
        })

        return self._baseSearch(_id=f"{artist_id}/albums?{query_params}",
                                return_type="artists")

    def artist_top_tracks(self, artist_id, country: str = "PH"):
        query_params = urlencode({
            "country": country
        })

        return self._baseSearch(_id=f"{artist_id}/top-tracks?{query_params}",
                                return_type="artists")

    def artist_related_artists(self, artist_id):
        return self._baseSearch(_id=f"{artist_id}/related-artists",
                                return_type="artists")

    # Search by query

    def search(self,
               q: str,
               type: str,
               market: str = "PH",
               limit: int = 20,
               offset: int = 0):
        """The Spotify Search Query

        Args:
            q (str, required): Search Query.
            type (str, required): Whether it's `track`, `artist` or `album`.
            market (str, optional): Search Market. Defaults to "PH".
            limit (int, optional): Search Limit. Defaults to 20.
            offset (int, optional): IDK. Defaults to 0.

        Raises:
            Exception: Query Cannot be None

        Returns:
            dict: The result

        """
        if q is None or type is None:
            raise Exception("query or type cannot be None.")
        query_params = urlencode({
            "q": q,
            "type": type,
            "market": market,
            "limit": limit,
            "offset": offset
        })
        return self._baseSearch(_id=f"?{query_params}", return_type="search")

    #  Others

#    def searchAlbumTracks(self, q=None):
#        """Search an album and return its tracks"""
#        search_result = self.search(q=q, type='album', market='PH', limit=1)
#        return self.album_tracks(search_result['albums']['items'][0]['id'],
# int(search_result['albums']['items'][0]['total_tracks']))

    # Users Profile
    # def my_user_profile(self):
    #     return self._baseSearch(_id="",return_type="me")
    # TODO we'll move this later

    def users(self, user_id):
        """Get a user's Profile

        Args:
         - user_id (str): Required. The user's ID or Spotify username.

        Returns:
         - dict: Returns a User's Spotify information.
        """
        return self._baseSearch(_id=user_id, return_type="users")

    def current_user(self):
        endpoint = "https://api.spotify.com/v1/me"
        r = requests.get(endpoint,
                         headers={
                             "Authorization": f"Bearer {self.access_token}"
                             })
        return r.json()

    def current_user_playing(self):
        endpoint = "https://api.spotify.com/v1/me/player/currently-playing"
        r = requests.get(endpoint,
                         headers={
                             "Authorization": f"Bearer {self.access_token}"
                             })
        return r.json()

    def current_user_top_tracks(self,
                                params_type: str,
                                limit: int = 20,
                                offset: int = 0,
                                time_range: str = "medium_term"):
        query_params = urlencode({"time_range": time_range,
                                  "limit": limit,
                                  "offset": offset})
        endpoint = "https://api.spotify.com/v1/me/top/"
        endpoint += f"{params_type}?{query_params}"
        r = requests.get(endpoint,
                         headers={
                             "Authorization": f"Bearer {self.access_token}"
                             })
        return r.json()

    # Player endpoint
    def addToQueue(self, uri: str, device_id: str = None):
        query_params = {
            'uri': uri
        }
        if device_id:
            query_params['device_id'] = device_id

        r = self._requests(requests.post, 'me/player/queue', query_params)

        if r.status_code != 204:
            if r.status_code == 404:
                raise SpotifyException(r.status_code,
                                       "Something went wrong in the\
 authentication", "NOT FOUND OR NO_ACTIVE_DEVICE")
            elif r.status_code == 403:
                raise SpotifyException(r.status_code,
                                       "Something went wrong in the\
 authentication", "FORBIDDEN OR PREMIUM REQUIRED")
        return

    def userAvailableDevice(self):
        """Get a User's Available Devices

        Returns:
            dict: Available devices
        """
        r = self._requests(requests.get, 'me/player/devices',)
        return r.json()

    def userPlayerInfo(self, market: str = None, additional_types: str = None):
        query_params = {}
        if market:
            query_params['market'] = market
        if additional_types:
            query_params['additional_types'] = additional_types

        r = self._requests(requests.get, 'me/player', query_params)

        return r.json()

    def userRecentTracks(self,
                         limit: int = 20,
                         after: int = None,
                         before: int = None):
        if after and before:
            raise Exception("Only one of before and after can be specified")

        query_params = {
            'limit': limit
        }
        if after:
            query_params['after'] = after
        if before:
            query_params['before'] = before

        r = self._requests(requests.get,
                           'me/player/recently-played',
                           query_params)
        return r.json()

    def userCurrentlyPlaying(self,
                             market: str = None,
                             additional_types: str = None):
        query_params = {}
        if market:
            query_params['market'] = market
        if additional_types:
            query_params['additional_types'] = additional_types

        r = self._requests(requests.get,
                           'me/player/currently-playing',
                           query_params)

        return r.json()

    def userPausePlayback(self, device_id: str = None):
        query_params = {}
        if device_id:
            query_params['device_id'] = device_id

        r = self._requests(requests.put, 'me/player/pause', query_params)

        if r.status_code != 204:
            status_code = ''
            if r.status_code == 404:
                status_code += f'{r.status_code} - NOT FOUND OR \
NO-ACTIVE-DEVICE'
            if r.status_code == 403:
                status_code += f'{r.status_code} - FORBIDDEN OR \
PREMIUM REQUIRED'
            raise Exception(f"An error occur. It must be none of your device is \
active or the player is already paused. {status_code}")

    def userSeekPlayback(self, position_ms: float, device_id: str = None):
        query_params = {
            'position_ms': position_ms
        }
        if device_id:
            query_params.update(device_id=device_id)

        self._requests(requests.put, 'me/player/seek', query_params)
        return

    def userSetRepeat(self, state: str, device_id: str = None):
        """Set Repeat Mode On User’s Playback

        `track` will repeat the current track. `context` will repeat the\
         current context. `off` will turn repeat off.

        Args:
            state (str): `track`, context or `off`
            device_id (str, optional): The id of the device this command is\
             targeting. If not supplied, the user’s currently active device is\
             the target. Defaults to None.
        """
        query_params = {
            'state': state
        }
        if device_id:
            query_params['device_id'] = device_id

        self._requests(requests.put, 'me/player/repeat', query_params)
        return

    def userSetVolume(self, volume_percent: int, device_id: str = None):
        query_params = {
            'volume_percent': volume_percent
        }
        if device_id:
            query_params.update(device_id=device_id)

        self._requests(requests.put, 'me/player/volume', query_params)
        return

    def nextTrack(self, device_id: str = None):
        query_params = None
        if device_id:
            query_params = {
                'device_id': device_id
            }

        self._requests(requests.post, 'me/player/next', query_params)
        return

    def previousTrack(self, device_id: str = None):
        query_params = None
        if device_id:
            query_params = {
                'device_id': device_id
            }

        self._requests(requests.post, 'me/player/previous', query_params)
        return

    # TODO
    def playTrack(self,
                  device_id: str = None,
                  context_uri: str = None,
                  uris: list = None,
                  offset=None,
                  position_ms: int = None):
        query_params = {}
        if device_id:
            query_params = {
                'device_id': device_id
            }

        data = {}
        if context_uri:
            data.update(context_uri=context_uri)
        if uris:
            data.update(uris=uris)
        if offset:
            data.update(offset=offset)
        if position_ms:
            data.update(position_ms=position_ms)

        return self._requests(requests.put,
                              'me/player/play',
                              query_params,
                              data)

    def userPlaybackShuffle(self, state: bool, device_id: str = None):
        query_params = {
            'state': state
        }
        if device_id is not None:
            query_params.update(device_id=device_id)

        self._requests(requests.put, 'me/player/shuffle', query_params)
        return

    def userMovePlayback(self, device_ids: list, play: bool = False):
        """	Transfer a User's Playback

            Transfer playback to a new device and determine if it should start\
             playing.

        Args:
            device_ids (list): A list of containing the ID of the device on\
             which playback should be started/transferred.
            play (bool, optional): true: ensure playback happens on new device\
             false or not provided: keep the current playback state.\
             Defaults to False.
        """
        data = {
            "device_ids": device_ids,
            "play": play
        }

        self._requests(requests.put, 'me/player', data=data)
        return
