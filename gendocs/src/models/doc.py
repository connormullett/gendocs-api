# doc.py

import enum

from . import db
from datetime import datetime
from marshmallow import fields, Schema
from marshmallow_enum import EnumField

from .comment import CommentModel, CommentSchema


class DocType(enum.Enum):
    TUTORIAL = 'tutorial'
    DEMO = 'demo'
    QUESTION = 'question'
    DOCUMENTATION = 'documentation'


class DocModel(db.Model):

    __tablename__ = 'docs'

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    doc_type = db.Column(db.Enum(DocType), nullable=False)
    language = db.Column(db.Text, nullable=False)
    comments = db.relationship('CommentModel', backref='docs', cascade='all, delete')
    likes = db.Column(db.Integer)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, data):
        self.owner_id = data.get('owner_id')
        self.title = data.get('title')
        self.doc_type = data.get('doc_type')
        self.language = data.get('language')
        self.content = data.get('content')
        self.created_at = datetime.utcnow()
        self.modified_at = datetime.utcnow()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.modified_at = datetime.utcnow()
        db.session.commit()

    @staticmethod
    def get_doc_types():
        return [doc_t.value for doc_t in DocType]

    @staticmethod
    def get_all_docs():
        return DocModel.query.all()

    @staticmethod
    def get_doc_by_id(id):
        return DocModel.query.get(id)
    
    @staticmethod
    def get_doc_by_name(name):
        return DocModel.query.get(name)

    @staticmethod
    def get_docs_by_type(doc_type):
        return DocModel.query.filter_by(doc_type=doc_type)

    @staticmethod
    def get_docs_by_language(language):
        return DocModel.query.filter_by(language=language)


class DocSchema(Schema):
    id = fields.Int(dump_only=True)
    owner_id = fields.Str(required=True)
    doc_type = EnumField(DocType)
    language = fields.Str(required=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    comments = fields.Nested(CommentSchema, many=True)
