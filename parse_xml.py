# -*- coding: utf-8 -*-

import os
import re

from app.models import RestInfo, AtrCity, AtrRecommendedFor, AtrMetro, AtrAverageBill, AtrFeatures, AtrTypes, AtrKitchens, QuickSearch 
from app import db
from lxml import etree

#new_entry = AtrCity(text_atr='test2')
#db.session.add(new_entry)
#db.session.commit()

#print AtrCity.query.all()
#print AtrCity.query.first().id_atr

XML_FILE = os.path.join(os.getcwd(), 'restaurants.xml')

try:
    parser = etree.XMLParser(recover=True)
    tree = etree.parse(XML_FILE, parser=parser)
    root = tree.getroot()

    print len(root)

    dicAtrCity = {}
    dicAtrRecommendedFor = {}
    dicAtrMetro = {}
    dicAtrAverageBill = {}
    dicAtrFeatures = {}
    dicAtrTypes = {}
    dicAtrKitchens = {}

    for restaurant in root:
        # for RestInfo
        id_rest = None
        name = None
        address = None
        url = None
        phone = None
        latitude = None
        longitude = None
        billMin = None
        billMax = None
        description = None
        photourl = None
        # for quicksearch
        city = None
        recommendedFor = []
        metro = None
        averageBill = None
        features = []
        types = []
        kitchens = []
        
        for element in restaurant:
            if element.tag == 'id':
                id_rest = element.text
            if element.tag == 'name':
                name = element.text
            if element.tag == 'address':
                address = element.text
            if element.tag == 'url':
                url = element.text
            if element.tag == 'phone':
                phone = element.text
            if element.tag == 'latitude':
                latitude = element.text
            if element.tag == 'longitude': 
                longitude = element.text
            if element.tag == 'billMin':
                billMin = element.text
            if element.tag == 'billMax':
                billMax = element.text
            if element.tag == 'description':
                description = element.text
                description = description[:description.find('<script')]
            if element.tag == 'gallery':
                try:
                    photourl = element[0].text
                except:
                    photourl = None
            if element.tag == 'city':
                city = element.text
            if element.tag == 'metro':
                metro = element.text
            if element.tag == 'attributes':
                for attrubute in element:
                    if attrubute.tag == 'recommendedFor':
                        for elementRecommendedFor in attrubute:
                            recommendedFor.append(elementRecommendedFor.text)
                    if attrubute.tag == 'features':
                        for elementFeatures in attrubute:
                            features.append(elementFeatures.text)
                    if attrubute.tag == 'types':
                        for elementTypes in attrubute:
                            types.append(elementTypes.text)
                    if attrubute.tag == 'kitchens':
                        for elementKitchens in attrubute:
                            kitchens.append(elementKitchens.text)

        #import pdb
        #pdb.set_trace()

        new_entry = RestInfo(id_rest=id_rest, name=name, address=address, url=url, phone=phone, latitude=latitude, longitude=longitude, billMin=billMin, billMax=billMax, description=description, photourl=photourl)
        db.session.add(new_entry)
        db.session.commit()
        
        try:
            average = (float(billMax) + float(billMin)) / 2
            if average <= 1000:
                averageBill = '0_1000'
            elif 1000 < average <= 2000:
                averageBill = '1000_2000'
            elif 2000 < average <= 3000:
                averageBill = '2000_3000'
            elif 3000 < average:
                averageBill = '3000'
        except:
            averageBill = 'unknown'
                
        # добавим новые элементы в таблицы сокращений имен аттрибутов
        
        if dicAtrCity.get(city) == None:
            if AtrCity.query.filter(AtrCity.text_atr==city).all() == []:
                new_entry = AtrCity(text_atr=city)
                db.session.add(new_entry)
                db.session.commit()
                dicAtrCity.update({city:AtrCity.query.filter(AtrCity.text_atr==city).all()[0].id_atr})
            
        
        for elementRecommendedFor in recommendedFor:
            if dicAtrRecommendedFor.get(elementRecommendedFor) == None:
                if AtrRecommendedFor.query.filter(AtrRecommendedFor.text_atr==elementRecommendedFor).all() == []:
                    new_entry = AtrRecommendedFor(text_atr=elementRecommendedFor)
                    db.session.add(new_entry)
                    db.session.commit()
                    dicAtrRecommendedFor.update({elementRecommendedFor:AtrRecommendedFor.query.filter(AtrRecommendedFor.text_atr==elementRecommendedFor).all()[0].id_atr})
        
        if dicAtrMetro.get(metro) == None:
            if AtrMetro.query.filter(AtrMetro.text_atr==metro).all() == []:
                new_entry = AtrMetro(text_atr=metro)
                db.session.add(new_entry)
                db.session.commit()
                dicAtrMetro.update({metro:AtrMetro.query.filter(AtrMetro.text_atr==metro).all()[0].id_atr})
        
        if dicAtrAverageBill.get(averageBill) == None:
            if AtrAverageBill.query.filter(AtrAverageBill.text_atr==averageBill).all() == []:
                new_entry = AtrAverageBill(text_atr=averageBill)
                db.session.add(new_entry)
                db.session.commit()
                dicAtrAverageBill.update({averageBill:AtrAverageBill.query.filter(AtrAverageBill.text_atr==averageBill).all()[0].id_atr})
            
        for elementFeatures in features:
            if dicAtrFeatures.get(elementFeatures) == None:
                if AtrFeatures.query.filter(AtrFeatures.text_atr==elementFeatures).all() == []:
                    new_entry = AtrFeatures(text_atr=elementFeatures)
                    db.session.add(new_entry)
                    db.session.commit()
                    dicAtrFeatures.update({elementFeatures:AtrFeatures.query.filter(AtrFeatures.text_atr==elementFeatures).all()[0].id_atr})
                
        for elementTypes in types:
            if dicAtrTypes.get(elementTypes) == None:
                if AtrTypes.query.filter(AtrTypes.text_atr==elementTypes).all() == []:
                    new_entry = AtrTypes(text_atr=elementTypes)
                    db.session.add(new_entry)
                    db.session.commit()
                    dicAtrTypes.update({elementTypes:AtrTypes.query.filter(AtrTypes.text_atr==elementTypes).all()[0].id_atr})
                
        for elementKitchens in kitchens:
            if dicAtrKitchens.get(elementKitchens) == None:
                if AtrKitchens.query.filter(AtrKitchens.text_atr==elementKitchens).all() == []:
                    new_entry = AtrKitchens(text_atr=elementKitchens)
                    db.session.add(new_entry)
                    db.session.commit()
                    dicAtrKitchens.update({elementKitchens:AtrKitchens.query.filter(AtrKitchens.text_atr==elementKitchens).all()[0].id_atr})
                
        print id_rest
        
        for elementRecommendedFor in recommendedFor:
            for elementFeatures in features:
                for elementTypes in types:
                    for elementKitchens in kitchens:
                        id_atr_city = dicAtrCity.get(city)
                        id_atr_recommend = dicAtrRecommendedFor.get(elementRecommendedFor)
                        id_atr_metro = dicAtrMetro.get(metro)
                        id_atr_averagebill = dicAtrAverageBill.get(averageBill)
                        id_atr_features = dicAtrFeatures.get(elementFeatures)
                        id_atr_types = dicAtrTypes.get(elementTypes)
                        id_atr_kitchens = dicAtrKitchens.get(elementKitchens)
                        new_entry = QuickSearch(id_rest=id_rest,
                                                city=id_atr_city,
                                                purpose=id_atr_recommend,
                                                metro=id_atr_metro,
                                                bill=id_atr_averagebill,
                                                features=id_atr_features,
                                                type=id_atr_types,
                                                kitchen=id_atr_kitchens)
                        db.session.add(new_entry)
            db.session.commit()
                
except IOError as e:
    print('nERROR - cant find file: %sn' % e)