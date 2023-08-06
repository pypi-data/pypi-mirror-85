from flask import Blueprint

bp = Blueprint('announce', __name__)

from . import routes