#import urllib.parse, urllib.request, urllib.error

import webapp2
import urllib, urllib2, webbrowser, json
import jinja2

import os
import logging



JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        logging.info("In MainHandler")
        #vals={}
        template_values = {}
        template_values['page_title'] = "myMixtape | Survey"
        template = JINJA_ENVIRONMENT.get_template('greetform.html')
        self.response.write(template.render(template_values))


def safeGet(url):
    try:

        return urllib2.urlopen(url)
    except urllib2.HTTPError as e:
        print ('The server couln\'t fulfill the request.')
        print ('Error code: ', e.code)
    except urllib2.URLError as e:
        print ('We failed to reach a server')
        print ('Reason: ', e.reason)
    return None

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
        encodedparams = urllib.urlencode(params)

        # request goes to POST https://accounts.spotify.com/api/token
        request = urllib2.Request('https://accounts.spotify.com/api/token', data=encodedparams, headers=headers)
        resp = urllib2.urlopen(request)

        respdata = json.load(resp)
        self.accessToken = respdata['access_token']


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
            fullurl = endpointurl + "?" + urllib.urlencode(params)

        headers = {"Authorization": "Bearer " + self.accessToken}
        request = urllib2.Request(fullurl, headers=headers)
        resp = urllib2.urlopen(request)

        return json.load(resp)


class GreetResponseHandlr(webapp2.RequestHandler):
    def post(self):
        vals = {}
        sclient = spotiClient()

        # sets vaiables to input
        limit = self.request.get('limit', 3)

        seed_genre = self.request.get('seed_genre')
        seed_danceability = self.request.get('seed_danceability')
        popularity = self.request.get('popularity')

        vals['page_title'] = "myMixtape | Survey"


        #searches for an artist ID to search in endpoint
        artist = self.request.get('seed_artist')
        artistID = sclient.apiRequest(endpoint="search", params={"q": artist, "type": "artist"})
        seed_artists = seed_artistID["artists"]["items"][0]["id"]

        # searches for track ID to search in endpoint
        track = self.request.get('seed_track')
        trackID = sclient.apiRequest(endpoint="search", params={"q": track, "type": "track"})
        seed_tracks = seed_trackID["tracks"]["items"][0]["id"]

        vals = {"limit": limit,"seed_genres": seed_genre,"target_danceability": target_danceability,
                 "target_popularity": popularity}

        searchresult = sclient.apiRequest(params=vals)

        vals['artistPlaylist'] = searchresult["tracks"][0]["artists"][0]['name']
        vals['trackPlaylist'] = searchresult["tracks"][0]['name']

        template = JINJA_ENVIRONMENT.get_template('greetresponse.html')
        self.response.write(template.render(vals))

application = webapp2.WSGIApplication([('/', MainHandler),('/gresponse', GreetResponseHandlr)], debug = True)











