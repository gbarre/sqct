import random
from flask import request
from models import Toss, toss_schema, tosses_schema, User
from app import db
from werkzeug.exceptions import BadRequest, NotFound
from sqlalchemy.exc import InvalidRequestError, StatementError


# GET /tosses
def search(filters):
    try:
        results = Toss.query.filter_by(**filters).all()
    except InvalidRequestError:
        raise BadRequest

    if not results:
        raise NotFound(description="No tosses have been found.")

    return tosses_schema.dump(results)


# POST /tosses
def post():
    toss_data = request.get_json()
    # data = toss_input_schema.load(toss_data)

    excludes = toss_data['excludes']
    users = User.query.filter(User.id.notin_(excludes)).all()

    elected = random.choice(users)

    toss = Toss(
        excludes=str(excludes),
        name=toss_data['name'],
        elected=elected.id
    )
    db.session.add(toss)
    db.session.commit()

    result = Toss.query.get(toss.id)
    result_data = toss_schema.dump(result)
    return result_data, 201, {
        'Location': f'{request.base_url}/tosses/{toss.id}',
    }


# GET /tosses/{tId}
def get(toss_id):
    try:
        toss = Toss.query.get(toss_id)
    except StatementError:
        raise BadRequest

    if toss is None:
        raise NotFound

    result_json = toss_schema.dump(toss)
    return result_json, 200, {
        'Location': f'{request.base_url}/tosses/{toss.id}'
    }


# DELETE /tosses/{tId}
def delete(toss_id):
    try:
        toss = Toss.query.get(toss_id)
    except StatementError:
        raise BadRequest

    if toss is None:
        raise NotFound

    db.session.delete(toss)
    db.session.commit()
    return None, 204
