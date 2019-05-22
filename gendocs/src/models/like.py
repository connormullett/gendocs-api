
from . import db
from marshmallow import fields, Schema

from .user import UserModel, UserSchema
from .doc import DocModel, DocSchema


class LikeModel(db.Model):

    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    doc_id = db.Column(db.Integer, db.ForeignKey('docs.id'), nullable=False)

    def __init__(self, data):
        self.owner_id = data.get('owner_id')
        self.doc_id = data.get('doc_id')

    def like(self):
        db.session.add(self)
        db.session.commit()
    
    def unlike(self):
        db.session.delete(self)
        db.session.commit()


class LikeSchema(Schema):
    owner_id = fields.Str(required=True)
    doc_id = fields.Int(required=True)
