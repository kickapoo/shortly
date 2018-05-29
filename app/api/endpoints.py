from . import api
from .responses import status_200, status_400
from .utils import get_raw_url, get_serialized_url, make_shorten, md5_hash

from ..models import ShortUrl

from flask import request, url_for


@api.route('/short-me', methods=['POST'])
def short_me():
    """
        Handling the creation of short url
    """
    # Check if request has the proper data
    raw_url, errors = get_raw_url(request)
    if errors:
        return status_400(errors=errors)

    # check if record exist with md5 of the rawurl
    qshorturl = ShortUrl.query.filter_by(
        raw_url_md5=md5_hash(raw_url)
    ).first()

    if qshorturl:
        # Url allready shorted
        return status_200(
            data={
                'srt_url': url_for('client.shorten_view',
                                   uuid=qshorturl.shorten_url,
                                   _external=True)
            }
        )

    # Serialize and process the shorter
    serialized_url, errors = get_serialized_url(raw_url)
    if errors:
        return status_400(errors=errors)

    # Create ShortUrl
    su = ShortUrl.create(
        raw_url=raw_url,
        raw_url_md5=md5_hash(raw_url),
        shorten_url=make_shorten(serialized_url.path),
    )

    return status_200(
        data={
            'srt_url': url_for('client.shorten_view',
                               uuid=su.shorten_url,
                               _external=True)
        }
    )
