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
        template_values={}
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
        limit = 10

        seed_genre = self.request.get('seed_genre')
        seed_danceability = self.request.get('seed_danceability')
        popularity = self.request.get('popularity')

        title = "myMixtape | Results"


        #searches for an artist ID to search in endpoint
        artist = self.request.get('seed_artist')
        artistID = sclient.apiRequest(endpoint="search", params={"q": artist, "type": "artist"})
        seed_artists = artistID["artists"]["items"][0]["id"]

        # searches for track ID to search in endpoint
        track = self.request.get('seed_track')
        trackID = sclient.apiRequest(endpoint="search", params={"q": track, "type": "track"})
        seed_tracks = trackID["tracks"]["items"][0]["id"]

        vals = {"seed_tracks": seed_tracks, "seed_artists": seed_artists, "title": title, "limit": limit,"seed_genres": seed_genre, "seed_danceability": seed_danceability, "target_popularity": popularity}

        recommendation = sclient.apiRequest(params = vals)

        # bad code to get all 10 songs, but for loops were not working well for me
        vals['artist1'] = recommendation["tracks"][0]["artists"][0]['name']
        vals['track1'] = recommendation["tracks"][0]['name']

        vals['artist2'] = recommendation["tracks"][0]["artists"][0]['name']
        vals['track2'] = recommendation["tracks"][1]['name']

        vals['artist3'] = recommendation["tracks"][2]["artists"][0]['name']
        vals['track3'] = recommendation["tracks"][2]['name']

        vals['artist4'] = recommendation["tracks"][3]["artists"][0]['name']
        vals['track4'] = recommendation["tracks"][3]['name']

        vals['artist5'] = recommendation["tracks"][4]["artists"][0]['name']
        vals['track5'] = recommendation["tracks"][4]['name']

        vals['artist6'] = recommendation["tracks"][5]["artists"][0]['name']
        vals['track6'] = recommendation["tracks"][5]['name']

        vals['artist7'] = recommendation["tracks"][6]["artists"][0]['name']
        vals['track7'] = recommendation["tracks"][6]['name']

        vals['artist8'] = recommendation["tracks"][7]["artists"][0]['name']
        vals['track8'] = recommendation["tracks"][7]['name']

        vals['artist9'] = recommendation["tracks"][8]["artists"][0]['name']
        vals['track9'] = recommendation["tracks"][8]['name']

        vals['artist10'] = recommendation["tracks"][9]["artists"][0]['name']
        vals['track10'] = recommendation["tracks"][9]['name']


        template = JINJA_ENVIRONMENT.get_template('greetresponse.html')
        self.response.write(template.render(vals))

application = webapp2.WSGIApplication([('/', MainHandler),('/gresponse', GreetResponseHandlr)], debug = True)











