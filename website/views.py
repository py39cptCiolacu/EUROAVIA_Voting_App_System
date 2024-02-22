from flask import Blueprint
from .models import Status


views_blueprint = Blueprint('views', __name__)

from .views_templates import home


def status():

    status = Status.query.order_by(Status.id.desc()).first()

    return status.status