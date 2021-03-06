# -*- coding: utf-8 -*-
from app import db


class SearchCriteria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(256))


class UserCreatedTextMapper(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    search_criteria = db.Column(db.Integer, db.ForeignKey('search_criteria.id'))
    user_text = db.Column(db.String(256), index=True)
    search_criteria_value = db.Column(db.Integer)


class RestInfo(db.Model):
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
        return u'<RestInfo: {}>'.format(self.id)


class AtrCity(db.Model):
    __tablename__ = 'atr_city'

    id_atr = db.Column(db.Integer, primary_key=True)
    text_atr = db.Column(db.String(64))

    def __repr__(self):
        return '<AtrCity {}>'.format(self.id_atr)


class AtrPurpose(db.Model):
    __tablename__ = 'atr_purpose'

    id_atr = db.Column(db.Integer, primary_key=True)
    text_atr = db.Column(db.String(256))


class AtrMetro(db.Model):
    __tablename__ = 'atr_metro'

    id_atr = db.Column(db.Integer, primary_key=True)
    text_atr = db.Column(db.String(256))

    def __repr__(self):
        return '<AtrMetro {}>'.format(self.id_atr)


class AtrBill(db.Model):
    __tablename__ = 'atr_bill'

    id_atr = db.Column(db.Integer, primary_key=True)
    text_atr = db.Column(db.String(256))


class AtrFeatures(db.Model):
    __tablename__ = 'atr_features'

    id_atr = db.Column(db.Integer, primary_key=True)
    text_atr = db.Column(db.String(2000))

    def __repr__(self):
        return '<AtrFeatures {}>'.format(self.id_atr)


class AtrTypes(db.Model):
    __tablename__ = 'atr_types'

    id_atr = db.Column(db.Integer, primary_key=True)
    text_atr = db.Column(db.String(2000))

    def __repr__(self):
        return '<AtrTypes {}>'.format(self.id_atr)


class AtrCuisine(db.Model):
    __tablename__ = 'atr_cuisine'

    id_atr = db.Column(db.Integer, primary_key=True)
    text_atr = db.Column(db.String(256))


class QuickSearch(db.Model):
    __tablename__ = 'quick_search'

    id = db.Column(db.Integer, primary_key=True)
    id_rest = db.Column(db.Integer, db.ForeignKey('rest_info.id_rest'))
    city = db.Column(db.Integer, db.ForeignKey('atr_city.id_atr'))
    purpose = db.Column(db.Integer, db.ForeignKey('atr_purpose.id_atr'))
    metro = db.Column(db.Integer, db.ForeignKey('atr_metro.id_atr'))
    bill = db.Column(db.Integer, db.ForeignKey('atr_bill.id_atr'))
    features = db.Column(db.Integer, db.ForeignKey('atr_features.id_atr'))
    type = db.Column(db.Integer, db.ForeignKey('atr_types.id_atr'))
    cuisine = db.Column(db.Integer, db.ForeignKey('atr_cuisine.id_atr'))

    def __repr__(self):
        return '<QuickSearch {}'.format(self.id_rest)