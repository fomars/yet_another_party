import json

import requests
import time

from app import app, redis
from flask import request
from models import *

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


def continue_session(sender_id, message_text):
    send_text_message(sender_id, 'I know what you did there')


def start_session(sender_id, message_text):
    if 'hi' in message_text.lower():
        redis.set(sender_id, {'started_at': int(time.time())})
        send_text_message(sender_id, 'Hi! Nice to meet you!')
    else:
        send_text_message(sender_id, 'Say hi!')


def received_msg(msg_event):
    sender_id = msg_event['sender']['id']
    recipient_id = msg_event['recipient']['id']
    timestamp = msg_event['timestamp']
    message = msg_event['message']
    app.logger.info('received message from user {}: {}'.format(sender_id, message))
    message_id = message['mid']
    message_text = message.get('text')
    message_attachments = message.get('attachments')

    if redis.get(sender_id):
        continue_session(sender_id, message_text)
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
