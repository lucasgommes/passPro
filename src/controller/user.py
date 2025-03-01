from flask import Blueprint, request
from src.main import User, db
from http import HTTPStatus


app = Blueprint("user",__name__, url_prefix="/users")


def create_user():
    data = request.json
    user = User(username=data["username"], password=data["password"])

    db.session.add(user)
    db.session.commit()


@app.route("/", methods=["POST", "GET"])
def handle_user():
    if request.method == "POST":
        create_user()
        return {'message': 'created user'}, HTTPStatus.CREATED
    else:
        return {
            'message': 'page GET'
        }
