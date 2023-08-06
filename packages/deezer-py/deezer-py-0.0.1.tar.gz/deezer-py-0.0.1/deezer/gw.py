import eventlet
requests = eventlet.import_patched('requests')

class LyricsStatus():
    """Explicit Content Lyrics"""

    NOT_EXPLICIT = 0
    """Not Explicit"""

    EXPLICIT = 1
    """Explicit"""

    UNKNOWN = 2
    """Unknown"""

    EDITED = 3
    """Edited"""

    PARTIALLY_EXPLICIT = 4
    """Partially Explicit (Album "lyrics" only)"""

    PARTIALLY_UNKNOWN = 5
    """Partially Unknown (Album "lyrics" only)"""

    NO_ADVICE = 6
    """No Advice Available"""

    PARTIALLY_NO_ADVICE = 7
    """Partially No Advice Available (Album "lyrics" only)"""

EMPTY_TRACK_DICT = {
    'SNG_ID': 0,
    'SNG_TITLE': '',
    'DURATION': 0,
    'MD5_ORIGIN': 0,
    'MEDIA_VERSION': 0,
    'FILESIZE': 0,
    'ALB_TITLE': "",
    'ALB_PICTURE': "",
    'ART_ID': 0,
    'ART_NAME': ""
}

class GW:
    def __init__(self, session, headers):
        self.http_headers = headers
        self.session = session

    def api_call(self, method, args=None, params=None):
        if args is None: args = {}
        if params is None: params = {}
        p = {'api_version': "1.0",
             'api_token': 'null' if method == 'deezer.getUserData' else self._get_token(),
             'input': '3',
             'method': method}
        p.update(params)
        try:
            result = self.session.post(
                "http://www.deezer.com/ajax/gw-light.php",
                params=p,
                timeout=30,
                json=args,
                headers=self.http_headers
            )
            result_json = result.json()
        except:
            eventlet.sleep(2)
            return self.api_call(method, args, params)
        if len(result_json['error']):
            raise APIError(json.dumps(result_json['error']))
        return result.json()['results']

    def _get_token(self):
        token_data = self.get_user_data()
        return token_data['checkForm']

    def get_user_data(self):
        return self.api_call('deezer.getUserData')

    def get_child_accounts(self):
        return self.api_call('deezer.getChildAccounts')

    def get_track(self, sng_id):
        return self.api_call('song.getData', {'sng_id': sng_id})

    def get_track_page(self, sng_id):
        return self.api_call('deezer.pageTrack', {'sng_id': sng_id})

    def get_track_lyrics(self, sng_id):
        return self.api_call('song.getLyrics', {'sng_id': sng_id})

    def get_tracks_gw(self, sng_ids):
        tracks_array = []
        body = self.api_call('song.getListData', {'sng_ids': sng_ids})
        errors = 0
        for i in range(len(sng_ids)):
            if sng_ids[i] != 0:
                tracks_array.append(body['data'][i - errors])
            else:
                errors += 1
                tracks_array.append(EMPTY_TRACK_DICT)
        return tracks_array

    def get_album(self, alb_id):
        return self.api_call('album.getData', {'alb_id': alb_id})

    def get_album_page(self, alb_id):
        return self.api_call('deezer.pageAlbum', {
                                'alb_id': alb_id,
                                'lang': 'en',
                                'header': True,
                                'tab': 0
                            })

    def get_album_tracks(self, alb_id):
        tracks_array = []
        body = self.api_call('song.getListByAlbum', {'alb_id': alb_id, 'nb': -1})
        for track in body['data']:
            _track = track
            _track['POSITION'] = body['data'].index(track)
            tracks_array.append(_track)
        return tracks_array

    def get_artist(self, art_id):
        return self.api_call('artist.getData', {'art_id': art_id})

    def get_artist_page(self, art_id):
        return self.api_call('deezer.pageArtist', {
                                'alb_id': art_id,
                                'lang': 'en',
                                'header': True,
                                'tab': 0
                            })

    def get_artist_top_tracks(self, art_id, limit=100):
        tracks_array = []
        body = self.api_call('artist.getTopTrack', {'art_id': art_id, 'nb': limit})
        for track in body['data']:
            track['POSITION'] = body['data'].index(track)
            tracks_array.append(track)
        return tracks_array

    def get_artist_discography(self, art_id, index=0, limit=25):
        return self.api_call('album.getDiscography', {
                                'art_id': art_id,
                                "discography_mode":"all",
                                'nb': limit,
                                'nb_songs': 0,
                                'start': index
                            })

    def get_playlist(self, playlist_id):
        return self.api_call('playlist.getData', {'playlist_id': playlist_id})

    def get_playlist_page(self, playlist_id):
        return self.api_call('deezer.pagePlaylist', {
                                'playlist_id': playlist_id,
                                'lang': 'en',
                                'header': True,
                                'tab': 0
                        })

    def get_playlist_tracks(self, playlist_id):
        tracks_array = []
        body = self.api_call('playlist.getSongs', {'playlist_id': playlist_id, 'nb': -1})
        for track in body['data']:
            track['POSITION'] = body['data'].index(track)
            tracks_array.append(track)
        return tracks_array

    def add_song_to_favorites(self, sng_id):
        return self.gw_api_call('favorite_song.add', {'SNG_ID': sng_id})

    def remove_song_from_favorites(self, sng_id):
        return self.gw_api_call('favorite_song.remove', {'SNG_ID': sng_id})

    def add_album_to_favorites(self, alb_id):
        return self.gw_api_call('album.addFavorite', {'ALB_ID': alb_id})

    def remove_album_from_favorites(self, alb_id):
        return self.gw_api_call('album.deleteFavorite', {'ALB_ID': alb_id})

    def add_artist_to_favorites(self, art_id):
        return self.gw_api_call('artist.addFavorite', {'ART_ID': art_id})

    def remove_artist_from_favorites(self, art_id):
        return self.gw_api_call('artist.deleteFavorite', {'ART_ID': art_id})

    def add_playlist_to_favorites(self, playlist_id):
        return self.gw_api_call('playlist.addFavorite', {'PARENT_PLAYLIST_ID': playlist_id})

    def remove_playlist_from_favorites(self, playlist_id):
        return self.gw_api_call('playlist.deleteFavorite', {'PLAYLIST_ID': playlist_id})

    def get_page(self, page):
        params = {
            'gateway_input': json.dumps({
                'PAGE': page,
                'VERSION': '2.3',
                'SUPPORT': {
                    'grid': [
                        'channel',
                        'album'
                    ],
                    'horizontal-grid': [
                        'album'
                    ],
                },
                'LANG': 'en'
            })
        }
        return self.api_call('page.get', params=params)

class APIError(Exception):
    """Base class for Deezer exceptions"""
    pass
