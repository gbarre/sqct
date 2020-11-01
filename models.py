import uuid
from datetime import datetime
from server import db, ma
from marshmallow import fields
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID


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
        db.string(32),
        nullable=False,
        unique=True,
        primary_key=True
    )
    name = db.Column(db.String(255), nullable=False, unique=True)
    tosses = db.relationship(
        "Tosse",
        backref="user",
        cascade="all, delete, delete-orphan",
        single_parent=True,
    )
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow
    )
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class Toss(db.Model):
    __tablename__ = "tosses"
    id = db.Column(GUID, nullable=False, unique=True,
                   default=uuid.uuid4, primary_key=True)
    elected = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.string(32), db.ForeignKey(
        'users.id'), nullable=True)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow
    )
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class UserSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    class Meta:
        model = User
        sqla_session = db.session

    id = ma.auto_field(dump_only=True)
    tosses = fields.Nested(
        "TossSchema",
        default=[],
        many=True,
    )
    created_at = ma.auto_field(dump_only=True)
    updated_at = ma.auto_field(dump_only=True)


class TossSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    class Meta:
        model = Toss
        include_relationships = False
        sqla_session = db.session

    created_at = ma.auto_field(dump_only=True)
    updated_at = ma.auto_field(dump_only=True)
