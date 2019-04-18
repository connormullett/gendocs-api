# doc.py

import enum

from . import db
from datetime import datetime
from marshmallow import fields, Schema
from marshmallow_enum import EnumField


class DocType(enum.Enum)
    TUTORIAL = 'tutorial'
    DEMO = 'demo'
    QUESTION = 'question'
    DOCUMENTATION = 'documentation'


class DocModel(db.Model):

    __tablename__ = 'docs'

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    doc_type = db.Column(db.Enum(DocType), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, data):
        self.owner_id = data.get('owner_id')
        self.title = data.get('title')
        self.doc_type = data.get('doc_type')
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
    def get_all_docs():
        return DocModel.query.all()

    @staticmethod
    def get_doc_by_id(id):
        return DocModel.query.get(id)

    @staticmethod
    def get_docs_by_type(doc_type)
        return DocModel.query.filter_by(doc_type=doc_type)


class DocSchema(Schema):
    id = fields.Int(dump_only=True)
    owner_id = fields.Int(required=True)
    doc_type = EnumField(DocType)
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)

