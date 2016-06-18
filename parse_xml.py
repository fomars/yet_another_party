# -*- coding: utf-8 -*-

import os
import re

from app.models import Rest_info, Atr_city, Atr_recommend, Atr_metro, Atr_averagebill, Atr_features, Atr_types, Atr_kitchens, Quick_search 
from app import db
from lxml import etree

#new_entry = Atr_city(text_atr='test2')
#db.session.add(new_entry)
#db.session.commit()

#print Atr_city.query.all()
#print Atr_city.query.first().id_atr

XML_FILE = os.path.join(os.getcwd(), 'restaurants.xml')

try:
    parser = etree.XMLParser(recover=True)
    tree = etree.parse(XML_FILE, parser=parser)
    root = tree.getroot()

    print len(root)

    for restaurant in root:
        # for rest_info
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
                #import pdb
                #pdb.set_trace()
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

        new_entry = Rest_info(id_rest=id_rest, name=name, address=address, url=url, phone=phone, latitude=latitude, longitude=longitude, billMin=billMin, billMax=billMax, description=description, photourl=photourl)
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
        
        if Atr_city.query.filter(Atr_city.text_atr==city).all() == []:
            new_entry = Atr_city(text_atr=city)
            db.session.add(new_entry)
            db.session.commit()    
        
        for elementRecommendedFor in recommendedFor:
            if Atr_recommend.query.filter(Atr_recommend.text_atr==elementRecommendedFor).all() == []:
                new_entry = Atr_recommend(text_atr=elementRecommendedFor)
                db.session.add(new_entry)
                db.session.commit()
        
        if Atr_metro.query.filter(Atr_metro.text_atr==metro).all() == []:
            new_entry = Atr_metro(text_atr=metro)
            db.session.add(new_entry)
            db.session.commit()
        
        if Atr_averagebill.query.filter(Atr_averagebill.text_atr==averageBill).all() == []:
            new_entry = Atr_averagebill(text_atr=averageBill)
            db.session.add(new_entry)
            db.session.commit()
            
        for elementFeatures in features:
            if Atr_features.query.filter(Atr_features.text_atr==elementFeatures).all() == []:
                new_entry = Atr_features(text_atr=elementFeatures)
                db.session.add(new_entry)
                db.session.commit()
                
        for elementTypes in types:
            if Atr_types.query.filter(Atr_types.text_atr==elementTypes).all() == []:
                new_entry = Atr_types(text_atr=elementTypes)
                db.session.add(new_entry)
                db.session.commit()
                
        for elementKitchens in kitchens:
            if Atr_kitchens.query.filter(Atr_kitchens.text_atr==elementKitchens).all() == []:
                new_entry = Atr_kitchens(text_atr=elementKitchens)
                db.session.add(new_entry)
                db.session.commit()
        print id_rest
        for elementRecommendedFor in recommendedFor:
            for elementFeatures in features:
                for elementTypes in types:
                    for elementKitchens in kitchens:
                        id_atr_city = Atr_city.query.filter(Atr_city.text_atr==city).all()[0].id_atr
                        id_atr_recommend = Atr_recommend.query.filter(Atr_recommend.text_atr==elementRecommendedFor).all()[0].id_atr
                        id_atr_metro = Atr_metro.query.filter(Atr_metro.text_atr==metro).all()[0].id_atr
                        id_atr_averagebill = Atr_averagebill.query.filter(Atr_averagebill.text_atr==averageBill).all()[0].id_atr
                        id_atr_features = Atr_features.query.filter(Atr_features.text_atr==elementFeatures).all()[0].id_atr
                        id_atr_types = Atr_types.query.filter(Atr_types.text_atr==elementTypes).all()[0].id_atr
                        id_atr_kitchens = Atr_kitchens.query.filter(Atr_kitchens.text_atr==elementKitchens).all()[0].id_atr
                        new_entry = Quick_search(id_rest=id_rest, id_atr_city=id_atr_city, id_atr_recommend=id_atr_recommend, id_atr_metro=id_atr_metro, id_atr_averagebill=id_atr_averagebill, id_atr_features=id_atr_features, id_atr_types=id_atr_types, id_atr_kitchens=id_atr_kitchens)
                        db.session.add(new_entry)
                        db.session.commit()
                
except IOError as e:
    print('nERROR - cant find file: %sn' % e)