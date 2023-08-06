import eventlet
requests = eventlet.import_patched('requests')
from deezer.gw import GW
from deezer.api import API

__version__ = "0.0.1"

class TrackFormats():
    """Number associtation for formats"""
    FLAC    = 9
    MP3_320 = 3
    MP3_128 = 1
    MP4_RA3 = 15
    MP4_RA2 = 14
    MP4_RA1 = 13
    DEFAULT = 8
    LOCAL   = 0

class Deezer:
    def __init__(self):
        self.http_headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                          "Chrome/79.0.3945.130 Safari/537.36",
            "Accept-Language": None
        }
        self.session = requests.Session()
        self.session.mount('http://', requests.adapters.HTTPAdapter(pool_maxsize=100))
        self.session.mount('https://', requests.adapters.HTTPAdapter(pool_maxsize=100))

        self.api = API(self.session, self.http_headers)
        self.gw = GW(self.session, self.http_headers)

    def set_accept_language(self, lang):
        self.http_headers['Accept-Language'] = lang

    def get_accept_language(self):
        return self.http_headers['Accept-Language']

    def get_countries_charts(self):
        temp = self.api.get_user_playlists('637006841')['data']
        result = sorted(temp, key=lambda k: k['title']) # Sort all playlists
        if not result[0]['title'].startswith('Top'): result = result[1:] # Remove loved tracks playlist
        return result

    def get_track_id_from_metadata(self, artist, track, album):
        artist = artist.replace("–", "-").replace("’", "'")
        track = track.replace("–", "-").replace("’", "'")
        album = album.replace("–", "-").replace("’", "'")

        resp = self.api.advanced_search(artist=artist, track=track, album=album, limit=1)
        if len(resp['data']) > 0: return resp['data'][0]['id']

        resp = self.api.advanced_search(artist=artist, track=track, limit=1)
        if len(resp['data']) > 0: return resp['data'][0]['id']

        # Try removing version
        if "(" in track and ")" in track and track.find("(") < track.find(")"):
            resp = self.api.advanced_search(artist=artist, track=track[:track.find("(")], limit=1)
            if len(resp['data']) > 0: return resp['data'][0]['id']
        elif " - " in track:
            resp = self.api.advanced_search(artist=artist, track=track[:track.find(" - ")], limit=1)
            if len(resp['data']) > 0: return resp['data'][0]['id']
        return "0"
