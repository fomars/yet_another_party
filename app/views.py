# coding=utf-8
import json

import datetime
import requests
import time

from app import app, redis
from flask import request

from app.helpers import get_restaurants, book_a_table
from models import *

FILTERS = ['city', 'purpose', 'metro', 'bill', 'features', 'cuisine']
EXAMPLES = [[u'Москва', u'Сочи', u'Санкт-Петербург'],
            [u'весело напиться', u'поужинать с девушкой', u'деловой обед', u'деловой ужин'],
            [u'Чеховская', u'Пушкинская'],
            [u'пятихат', u'тысяча', u'тыща', u'недорого'],
            [u'wifi', u'веранда', u'на набережной', u'с детьми', u'парковка', u'баркас'],
            [u'грузинская', u'русская' u'украинская']]
GREETINGS = ['choose {}'.format(f) for f in FILTERS]

PROMPTS = [{'name': 'time', 'formatter': lambda s: int(
    (datetime.datetime.strptime('2016 ' + s, '%Y %d.%m %H:%M') - datetime.datetime(1970, 1, 1)).total_seconds())},
           {'name': 'firstName', 'formatter': lambda s: unicode(s)},
           {'name': 'persons', 'formatter': lambda s: int(s)},
           {'name': 'phone', 'formatter': lambda s: unicode(s)}]
PROMPT_GREETINGS = ['enter datetime DD.mm HH:MM',
                    'enter your name',
                    'enter the number of persons',
                    'enter your phone']


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
    def __init__(self, title, image_url=None, subtitle=None, buttons=None):
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
    params = {k: v for k, v in kwargs.items() if k in FILTERS}
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
    """

    :type restaurants: list[RestInfo]
    """
    bubbles = [Element(r.name,
                       image_url=r.photourl,
                       buttons=[PostbackButton(u'забронировать', '{}'.format(r.id_rest))]) for r in
               restaurants]
    template = GenericMessageTemplate(bubbles)
    template.send(sender_id)


def report_nothing_found(user_id, examples):
    send_text_message(user_id, u'К сожалению по вашему запросу ничего не найдено. \
    Попробуйте еще раз, например: {}'.format(', '.join(examples)))


def process_filter(filter_id, user_id, message_text):
    try:
        f = FILTERS[filter_id]
    except IndexError:
        send_text_message(user_id, 'I know what you did there')
    res = get_restaurants(user_id, **{f: message_text})
    if res:
        show_results(user_id, res[0:5])
        go_to_next_filter(user_id, f=message_text)
    else:
        report_nothing_found(user_id, EXAMPLES[filter_id])


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
    redis.hmset(sender_id, {'started_at': int(time.time())})
    update_session(sender_id, next_filter=0)
    return continue_session(sender_id, redis.hgetall(sender_id), message_text)


def process_prompt(next_prompt, user_id, message_text):
    if next_prompt < len(PROMPTS):
        prompt = PROMPTS[next_prompt]
        value = prompt['formatter'](message_text)
        redis.hset(user_id, prompt['name'], value)
        redis.hset(user_id, 'next_prompt', next_prompt+1)
        redis.expire(user_id, app.config['EXPIRE'])
        if next_prompt < len(PROMPTS):
            send_text_message(user_id, PROMPT_GREETINGS[next_prompt+1])
        return

    res = book_a_table(redis.hget(user_id, 'id_rest'),
                 redis.hget(user_id, 'time'),
                 redis.hget(user_id, 'persons'),
                 redis.hget(user_id, 'firstName'),
                 redis.hget(user_id, 'phone'))
    send_text_message(user_id, str(res))


def continue_session(user_id, session, message_text):
    ready = session.get('ready')
    if ready:
        next_prompt = int(session.get('next_prompt', 0))
        return process_prompt(next_prompt, user_id, message_text)
    else:
        next_filter = int(session.get('next_filter', 0))
        return process_filter(next_filter, user_id, message_text)


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


def prompt_user(user_id, session):
    pass


def start_prompt_user(sender_id, id_rest):
    redis.hset(sender_id, 'next_prompt', 0)
    redis.hset(sender_id, 'ready', 1)
    redis.hset(sender_id, 'id_rest', id_rest)
    redis.expire(sender_id, app.config['EXPIRE'])
    send_text_message(sender_id, PROMPT_GREETINGS[0])


def received_postback(msg_event):
    """

    :param msg_event:
    :return:
    """
    sender_id = msg_event['sender']['id']
    recipient_id = msg_event['recipient']['id']
    timestamp = msg_event['timestamp']
    postback = msg_event['postback']

    if 'payload' in postback:
        id_rest = int(postback['payload'])
        start_prompt_user(sender_id, id_rest)
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
        for entry in data['entry'][0:3]:
            page_id = entry['id']
            time_of_event = entry['time']
            for msg_event in entry['messaging'][0:3]:
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
