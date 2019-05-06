# models/user.py

from marshmallow import fields, Schema
from datetime import datetime
from . import db
from ..app import bcrypt

from .doc import DocSchema
from .comment import CommentSchema


class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    docs = db.relationship('DocModel', backref='users', cascade='all, delete-orphan', lazy=True)
    comments = db.relationship('CommentModel', backref='users', cascade='all, delete-orphan', lazy=True)

    def __init__(self, data):
        self.name = data.get('name')
        self.email = data.get('email')
        self.password = self._generate_hash(data.get('password'))
        self.created_at = datetime.utcnow()
        self.modified_at = datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            if key == 'password':
                self.password = self._generate_hash(value)
            setattr(self, key, item)
        self.modified_at = datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def _generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode('utf-8')

    def _check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @staticmethod
    def get_all_users():
        return UserModel.query.all()

    @staticmethod
    def get_user_by_id(id):
        return UserModel.query.get(id)

    @staticmethod
    def get_user_by_name(name):
        return UserModel.query.filter_by(name=name).first()

    @staticmethod
    def get_user_by_email(value):
        return UserModel.query.filter_by(email=value).first()


# models/user.py
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    docs = fields.Nested(DocSchema, many=True)
    comments = fields.Nested(CommentSchema, many=True)

