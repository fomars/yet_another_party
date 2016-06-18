# -*- coding: utf-8 -*-
from app import db

class Attribute(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<Attribute {}>'.format(self.text)


class AttributeMapper(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    attribute_id = db.Column(db.Integer, db.ForeignKey('attribute.id'))
    text = db.Column(db.String(64), index=True)
    attribute_value_id = db.Column(db.Integer, index=True)
    
    def __repr__(self):
        return '<AttributeMapper {}-{}>'.format(self.text, self.attribute_value_id)
        
        
class Rest_info(db.Model):
    __tablename__ = 'rest_info'

    id = db.Column(db.Integer, primary_key=True)
    id_rest = db.Column(db.Integer, index=True) 
    name = db.Column(db.String(256)) 
    address = db.Column(db.String(256))
    url = db.Column(db.String(256)) 
    phone = db.Column(db.String(64)) 
    latitude = db.Column(db.String(64)) 
    longitude = db.Column(db.String(64))
    billMin = db.Column(db.String(64)) 
    billMax = db.Column(db.String(64))
    description = db.Column(db.String(4096))
    photourl = db.Column(db.String(256))

    def __repr__(self):
        return u'<Rest_info: {}>'.format(self.id)


class Atr_city(db.Model):
    __tablename__ = 'atr_city'

    id_atr = db.Column(db.Integer, primary_key=True)
    text_atr = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<Atr_city {}>'.format(self.id_atr)


class Atr_recommend(db.Model):
    __tablename__ = 'atr_recommend'

    id_atr = db.Column(db.Integer, primary_key=True)
    text_atr = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<Atr_recommend {}>'.format(self.id_atr)


class Atr_metro(db.Model):
    __tablename__ = 'atr_metro'

    id_atr = db.Column(db.Integer, primary_key=True)
    text_atr = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<Atr_metro {}>'.format(self.id_atr)


class Atr_averagebill(db.Model):
    __tablename__ = 'atr_averagebill'

    id_atr = db.Column(db.Integer, primary_key=True)
    text_atr = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<Atr_averagebill {}>'.format(self.id_atr)


class Atr_features(db.Model):
    __tablename__ = 'atr_features'

    id_atr = db.Column(db.Integer, primary_key=True)
    text_atr = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<Atr_features {}>'.format(self.id_atr)


class Atr_types(db.Model):
    __tablename__ = 'atr_types'

    id_atr = db.Column(db.Integer, primary_key=True)
    text_atr = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<Atr_types {}>'.format(self.id_atr)


class Atr_kitchens(db.Model):
    __tablename__ = 'atr_kitchens'

    id_atr = db.Column(db.Integer, primary_key=True)
    text_atr = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<Atr_kitchens {}>'.format(self.id_atr)


class Quick_search(db.Model):
    __tablename__ = 'quick_search'

    id = db.Column(db.Integer, primary_key=True)
    id_rest = db.Column(db.Integer, index=True)
    id_atr_city = db.Column(db.Integer, index=True)
    id_atr_recommend = db.Column(db.Integer, index=True)
    id_atr_metro = db.Column(db.Integer, index=True)
    id_atr_averagebill = db.Column(db.Integer, index=True)
    id_atr_features = db.Column(db.Integer, index=True)
    id_atr_types = db.Column(db.Integer, index=True)
    id_atr_kitchens = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<Quick_search {}'.format(self.id_rest)