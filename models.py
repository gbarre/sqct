import uuid
from datetime import datetime
from app import db, ma
from marshmallow import fields, post_dump
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID
from ast import literal_eval


class GUID(TypeDecorator):
    """Platform-independent GUID type.

    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.

    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())  # pragma: no cover
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)  # pragma: no cover
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value


class User(db.Model):
    __tablename__ = "users"
    __default_filter__ = "name"

    id = db.Column(  # LDAP UID
        db.String(32),
        nullable=False,
        unique=True,
        primary_key=True
    )
    name = db.Column(db.String(255), nullable=False, unique=True)
    tosses = db.relationship(
        "Toss",
        backref="user",
        cascade="all, delete, delete-orphan",
        single_parent=True,
    )


class Toss(db.Model):
    __tablename__ = "tosses"
    id = db.Column(GUID, nullable=False, unique=True,
                   default=uuid.uuid4, primary_key=True)
    elected = db.Column(db.String(32), db.ForeignKey(
        'users.id'), nullable=True)
    excludes = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(255), nullable=True)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow
    )


class UserSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = User
        include_relationships = False
        sqla_session = db.session

    id = ma.auto_field(dump_only=True)
    tosses = fields.Nested(
        "TossSchema",
        default=[],
        many=True,
    )


class TossSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Toss
        include_relationships = True
        include_fk = True
        sqla_session = db.session
        exclude = ('user',)

    id = ma.auto_field(dump_only=True)
    created_at = ma.auto_field(dump_only=True)

    @post_dump()
    def __post_dump(self, data, **kwargs):
        if 'excludes' in data:
            data['excludes'] = literal_eval(data['excludes'])
        return data


user_schema = UserSchema()
users_schema = UserSchema(many=True)
toss_schema = TossSchema()
tosses_schema = TossSchema(many=True)
