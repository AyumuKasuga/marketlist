# coding: utf-8
from google.appengine.api.urlfetch import fetch
from simplejson import dumps, loads


def get_short_link(url):
    res = fetch(url='https://www.googleapis.com/urlshortener/v1/url', method='POST',
                headers={'Content-Type': 'application/json'},
                payload=dumps({"longUrl": url}))
    try:
        return loads(res.content)['id']
    except:
        return False
