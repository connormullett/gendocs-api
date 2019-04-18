# comment.py

from . import db
from datetime import datetime

from marshmallow import fields, Schema


class CommentModel(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    reply_to = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, data):
        self.id = data.get('id')
        self.owner_id = data.get('owner_id')
        self.content = data.get('content')
        self.reply_to = data.get('reply_to')
        self.created_at = datetime.utcnow()
        self.modified_at = datetime.utcnow()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items()
            setattr(self, key, item)
        self.modified_at = datetime.utcnow()
        db.session.commit()

    # TODO: potentially dont need query tools for comments



class CommentSchema(Schema):
    pass

