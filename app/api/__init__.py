from flask import Blueprint
from app.api.decorators import accepts_only_json_request

api = Blueprint('api', __name__)


@api.before_request
@accepts_only_json_request
def before_request():
    pass


from .endpoints import * #noqa
