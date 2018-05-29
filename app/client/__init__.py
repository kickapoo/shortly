from flask import Blueprint
from flask import render_template, current_app, redirect
from app.models import ShortUrl

client = Blueprint('client', __name__)


@client.route("/")
def index():
    return render_template("index.html", title=current_app.config['APP_NAME'])


@client.route('/<uuid>', methods=['GET'])
def shorten_view(uuid):
    qshorturl = ShortUrl.query.filter_by(
        shorten_url=uuid
    ).first()
    if qshorturl:
        return redirect(qshorturl.raw_url)
    return render_template("404.html", title=current_app.config['APP_NAME'])
