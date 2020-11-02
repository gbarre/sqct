from models import User, user_schema, users_schema
from werkzeug.exceptions import BadRequest, NotFound
from sqlalchemy.exc import InvalidRequestError


# GET /users
def search(filters):
    # if user.role < RoleEnum.admin:
    #     results = [user]
    # else:
    try:
        results = User.query.filter_by(**filters).all()
    except InvalidRequestError:
        raise BadRequest

    if not results:
        raise NotFound(description="No users have been found.")

    return users_schema.dump(results)


# GET /users/{uId}
def get(user_id):
    requested_user = User.query.filter_by(id=user_id).first()

    if requested_user is None:
        raise NotFound(description=f"The requested user '{user_id}' "
                                   "has not been found.")

    # if (user.role == RoleEnum.user) and (user.name != user_id):
    #     raise Forbidden

    return user_schema.dump(requested_user)
