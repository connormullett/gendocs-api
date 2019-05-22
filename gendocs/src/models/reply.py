
from . import db
from datetime import datetime
from marshmallow import fields, Schema


class ReplyModel(db.Model):

    __tablename__ = 'replies'

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    reply_to = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=False)
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
        for key, item in data.items():
            setattr(self, key, item)
        self.modified_at = datetime.utcnow()
        db.session.commit()
    
    @staticmethod
    def get_reply_by_id(reply_id):
        return ReplyModel.query.filter_by(id=reply_id).first()

    @staticmethod
    def get_replies_by_user(user_id):
        return ReplyModel.query.filter_by(owner_id=user_id)

    @staticmethod
    def get_replies_by_comment_id(comment_id):
        return ReplyModel.query.filter_by(reply_to=comment_id)


class ReplySchema(Schema):
    id = fields.Int(dump_only=True)
    owner_id = fields.Str(required=True)
    content = fields.Str(required=True)
    reply_to = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
