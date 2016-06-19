# coding=utf-8
import json

import requests
import time

from app import app, redis
from flask import request

from app.helpers import get_restaurants
from models import *

FILTERS = ['city', 'purpose', 'metro', 'bill', 'features', 'type', 'cuisine']
GREETINGS = ['choose {}'.format(f) for f in FILTERS]


def received_authentication(msg_event):
    pass


def call_send_api(message_data):
    r = requests.post('https://graph.facebook.com/v2.6/me/messages',
                      data=message_data,
                      params={'access_token': app.config['ACCESS_TOKEN']},
                      headers={'Content-Type': 'application/json'})
    app.logger.info('response: {}'.format(r.content))


def send_text_message(recipient_id, text):
    message_data = json.dumps({
        'recipient': {
            'id': recipient_id
        },
        'message': {
            'text': text
        }
    })
    call_send_api(message_data)


class PostbackButton(object):

    def __init__(self, title, payload):
        self.title = title
        self.payload = payload

    def dict(self):
        return {'title': self.title,
                'type': 'postback',
                'payload': self.payload}


class Element(object):
    def __init__(self, title, url=None, image_url=None, subtitle=None, buttons=None):
        self.title = title
        self.image_url = image_url
        self.subtitle = subtitle
        self.buttons = buttons

    def dict(self):
        return {'title': self.title,
                'image_url': self.image_url,
                'subtitle': self.subtitle,
                'buttons': [b.dict() for b in self.buttons]}


class GenericMessageTemplate(object):
    def __init__(self, elements):
        """

        :type elements: list[Element]
        """
        self.elements = elements

    def dict(self):
        return {"attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [e.dict() for e in self.elements]}
        }}

    def send(self, recipient_id):
        msg_data = json.dumps({"recipient": {"id": recipient_id},
                               "message": self.dict()})
        return call_send_api(msg_data)


def update_session(user_id, next_filter=None, **kwargs):
    if next_filter is not None:
        redis.hset(user_id, 'next_filter', next_filter)
    params = {k: v for k,v in kwargs.items() if k in FILTERS}
    if params:
        redis.hmset(user_id, params)
    redis.expire(user_id, app.config['EXPIRE'])


def update_session_inc(user_id, **kwargs):
    next_filter = int(redis.hget(user_id, 'next_filter')) + 1
    update_session(user_id, next_filter=next_filter, **kwargs)


def go_to_next_filter(user_id, **kwargs):
    try:
        next_filter = int(redis.hget(user_id, 'next_filter')) + 1
    except TypeError:
        next_filter = 0
    send_text_message(user_id, GREETINGS[next_filter])
    update_session(user_id, next_filter=next_filter, **kwargs)


def show_results(sender_id, restaurants):
    bubbles = [Element(r['name'], buttons=[PostbackButton(u'забронировать', 'book {}'.format(r['id']))]) for r in
               restaurants]
    template = GenericMessageTemplate(bubbles)
    template.send(sender_id)


def report_nothing_found(user_id, examples):
    send_text_message(user_id, u'К сожалению по вашему запросу ничего не найдено. \
    Попробуйте еще раз, например: {}'.format(', '.join(examples)))


def process_city(sender_id, message_text):
    res = get_restaurants(sender_id, city=message_text)
    ids = [r['id'] for r in res]
    if ids:
        show_results(sender_id, res)
        go_to_next_filter(sender_id, city=message_text)
    else:
        report_nothing_found(sender_id, [u'Сочи', u'Омск'])


def process_property(user_id, message_text):
    send_text_message(user_id, 'Property processing there')


def start_session(sender_id, message_text):
    # if 'hi' in message_text.lower():
    #     redis.set(sender_id, {'started_at': int(time.time())})
    #     send_text_message(sender_id, 'Hi! Nice to meet you!')
    # else:
    #     send_text_message(sender_id, 'Say hi!')
    redis.hmset(sender_id, {'started_at': int(time.time())})
    update_session(sender_id, next_filter=0)
    # return process_city(sender_id, message_text)
    return continue_session(sender_id, redis.hgetall(sender_id), message_text)


def continue_session(user_id, session, message_text):
    actions = {0: process_city,
               1: process_property}
    next_filter = int(session.get('next_filter', 0))
    action = actions.get(next_filter)
    if action:
        return action(user_id, message_text)
    else:
        send_text_message(user_id, 'I know what you did there')


def received_msg(msg_event):
    sender_id = msg_event['sender']['id']
    recipient_id = msg_event['recipient']['id']
    timestamp = msg_event['timestamp']
    message = msg_event['message']
    app.logger.info('received message from user {}: {}'.format(sender_id, message))
    message_id = message['mid']
    message_text = message.get('text')
    message_attachments = message.get('attachments')

    session = redis.hgetall(sender_id)
    if session:
        continue_session(sender_id, session, message_text)
    else:
        start_session(sender_id, message_text)


def recieved_delivery_confirmation(msg_event):
    pass


def received_postback(msg_event):
    pass


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # pdb.set_trace()
    if request.method == 'POST' and request.json['object'] == 'page':
        data = request.json
        # app.process_response(app.make_response('ok'))
        for entry in data['entry']:
            page_id = entry['id']
            time_of_event = entry['time']
            for msg_event in entry['messaging']:
                if msg_event.get('optin'):
                    received_authentication(msg_event)
                elif msg_event.get('message'):

                    received_msg(msg_event)

                elif msg_event.get('delivery'):
                    recieved_delivery_confirmation(msg_event)
                elif msg_event.get('postback'):
                    received_postback(msg_event)
                else:
                    print('Webhook received unknown messaging event: {}'.format(msg_event))
        return 'ok'

    if request.args['hub.verify_token'] == 'huyarker':
        return request.args['hub.challenge']
    else:
        return 'give me verify token'
