import urllib.request, urllib.parse, urllib.error
import json


class spotiClient():
    def __init__(self):
        self.accessToken = None
        self.spotifyAuth()

    def spotifyAuth(self):
        """Method to actually handle authorization"""

        from secrets import CLIENT_ID, CLIENT_SECRET
        import base64

        # build the header
        authorization = base64.standard_b64encode((CLIENT_ID + ':' + CLIENT_SECRET).encode())
        headers = {"Authorization": "Basic " + authorization.decode()}

        # encode the params dictionary, note it needs to be byte encoded
        params = {"grant_type": "client_credentials"}
        encodedparams = urllib.parse.urlencode(params).encode()

        # request goes to POST https://accounts.spotify.com/api/token
        request = urllib.request.Request('https://accounts.spotify.com/api/token', data=encodedparams, headers=headers)
        resp = urllib.request.urlopen(request)

        # I should do some error handling, but this is a quick example
        respdata = json.load(resp)
        self.accessToken = respdata['access_token']

        # Note that by default this token will expire in 60 minutes.
        # If your application will run longer, you will need a way to manage that.



    def apiRequest(self, version="v1", endpoint="recommendations", item=None, params=None):
        """Method for API calls once authorized. By default, it will execute a search.

        See https://developer.spotify.com/web-api/endpoint-reference/ for endpoints

        Items, e.g., a track ID, are passed in via the item parameter.
        Parameters, e.g., search parameters, are passed in via the params dictionary"""

        if self.accessToken is None:
            print("Sorry, you must have an access token for this to work.")
            return {}

        baseurl = "https://api.spotify.com/"
        endpointurl = "%s%s/%s" % (baseurl, version, endpoint)

        # are there any params we need to pass in?
        if item is not None:
            endpointurl = endpointurl + "/" + item
        if params is not None:
            fullurl = endpointurl + "?" + urllib.parse.urlencode(params)

        headers = {"Authorization": "Bearer " + self.accessToken}
        request = urllib.request.Request(fullurl, headers=headers)
        resp = urllib.request.urlopen(request)

        return json.load(resp)


sclient = spotiClient()
#searchresult = sclient.apiRequest(params={"type": "artist", "q": "weeknd"})

limit = 3
market = "US"
seed_genre = "hip-hop"
target_acousticness= 0.5
target_danceability = 0.5
target_energy = 0.5
target_instrumentalness = 0.5
target_liveness = 0.5
popularity = 50
speechiness = 0.5

artist = "adele"
seed_artist = sclient.apiRequest(endpoint="search", params={"q": artist,"type":"artist"})
artist = seed_artist["artists"]["items"][0]["id"]

track = "hello"
seed_track = sclient.apiRequest(endpoint="search", params={"q" :track,"type":"track"})
track = seed_track["tracks"]["items"][0]["id"]


input = {"limit": limit, "market": market, "seed_genres": seed_genre, "target_acousticness": target_acousticness, "target_danceability": target_danceability, "target_energy": target_energy, "target_instrumentalness": target_instrumentalness, "target_liveness": target_liveness, "target_popularity": popularity, "target_speechiness":speechiness}


searchresult = sclient.apiRequest(params = input)


print(searchresult["tracks"][0]["artists"][0]['name'])
print(searchresult["tracks"][0]['name'])

print(searchresult["tracks"][1]["artists"][0]['name'])
print(searchresult["tracks"][1]['name'])

print(searchresult["tracks"][2]["artists"][0]['name'])
print(searchresult["tracks"][2]['name'])

