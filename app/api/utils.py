import re
import validus
import urllib
import hashlib
import uuid
from collections import OrderedDict

from app.models import WordList


def md5_hash(string):
    """
        Return md5 has for a string (force encode utf-8)
    """
    return hashlib.md5(string.encode('utf-8')).hexdigest()


def generate_hash():
    """
        Generate a eight long uuid
    """
    return str(uuid.uuid4().hex[:8])


def get_raw_url(request):
    """
        Get request data with related errors if exists.
    """
    # pitfall working with axios lib. By default the request/ response schema
    # has structure with data as key
    data = request.get_json(silent=True)['data']
    if not data:
        return None, ['Empty request']
    raw_url = data.get('raw_lng_url', None)
    if not raw_url:
        return None, ['Missing Url']
    if not validus.isurl(raw_url):
        return None, ['Invalid url syntax']
    return raw_url, []


def get_serialized_url(raw_url):
    """
        Check if url path exists in a raw_url
    """
    url_serializer = urllib.parse.urlsplit(raw_url)
    if url_serializer.path in ['', '/', None]:
        return None, ['Please provide a long url with a path']
    return url_serializer, None


def make_shorten(path):
    """
        Return the shorten path of the shorten url
    """
    # split path and remove empty
    p_split_with_clean_spaces = ''.join(list(filter(None, path.split('/'))))
    # remove any special chars like "."
    p_clean_special = re.sub('[^A-Za-z0-9]+', '', p_split_with_clean_spaces)
    first_letters = list(OrderedDict.fromkeys(p_clean_special))

    found = False
    for fl in first_letters:
        w = WordList.query.order_by(WordList.first_letter).filter(
            (WordList.first_letter == fl) & (WordList.active == False)
        ).first()
        if w:
            found = True
            break

    if found:
        w.update(active=True)
        return w.word
    # if all fail, generate hash
    return generate_hash()
