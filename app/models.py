from app import db


class Attributes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(64), index=True)


class Attributes_mapper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attribute_id = db.Column(db.Integer)
    text = db.Column(db.String(64), index=True)
    attribute_value_id = db.Column(db.Integer, index=True)


