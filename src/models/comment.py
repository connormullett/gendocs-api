# comment.py

from . import db
from datetime import datetime
from marshmallow import fields, Schema

# from .reply import ReplyModel


class CommentModel(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    doc_id = db.Column(db.Integer, db.ForeignKey('docs.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, data):
        self.id = data.get('id')
        self.owner_id = data.get('owner_id')
        self.doc_id = data.get('doc_id')
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
    def get_all_comments_by_doc_id(doc_id):
        return CommentModel.query.filter_by(doc_id=doc_id)

    @staticmethod
    def get_replies_from_comment_id(comment_id):
        pass


class CommentSchema(Schema):
    id = fields.Int(dump_only=True)
    owner_id = fields.Int(required=True)
    doc_id = fields.Int(required=True)
    content = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)

