import json

import requests

from app import app
from flask import request


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


def received_msg(msg_event):
    sender_id = msg_event['sender']['id']
    recipient_id = msg_event['recipient']['id']
    timestamp = msg_event['timestamp']
    message = msg_event['message']
    app.logger.info('received message from user {}: {}'.format(sender_id, message))
    message_id = message['mid']
    message_text = message.get('text')
    message_attachments = message.get('attachments')

    if message_text:
        if 'hi' in message_text.lower():
            send_text_message(sender_id, 'Hi! Nice to meet you!')
        else:
            send_text_message(sender_id, 'Say hi!')


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
        for entry in data['entry']:
            page_id = entry['id']
            time_of_event = entry['time']
            app.logger.info((page_id, time_of_event))
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
