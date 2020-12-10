from app import app
from flask import make_response, request

import json
import requests

WEBHOOK_VERIFY_TOKEN = 'test_faq_token'
PAGE_ACCESS_TOKEN = 'EAAeeVSYcYQYBAHng9dsVAiRdvy1kKttTvWFkcmoU2fwUr44vnJXVQJfXzuZCL8FAUM9IqZCqlZBgaWMbRw6JQ09xlF9s130Syzt1trfbZCC1jxbM4IHtPqxVXRg6DB11rsDheteFCtLuXHqJWTXqHkz4gMV7QZBRATgucFmF2ywZDZD'
#this is for page Page_thread_queue_test
PAGE_ACCESS_TOKEN2 = 'EAAeeVSYcYQYBAOVAMY6T8t6htQMnJ3gGZBfq9H7VsvRaazNsqJ6FIfsIYK2GBAWRNrFzyB95BADbeZBZClDP6Vdf7Jp7gtpYIIur4oPZCBl4VXpAf3P4kjM8ldR3heOXbUZCFBzvk6rfB0iTPOlqhSKUySb8afVp8rLNnBMR1O0E71D1vfOlvAu3g0lvGRAkZD'
PATs = {
  "620697518375534": "EAAeeVSYcYQYBAHng9dsVAiRdvy1kKttTvWFkcmoU2fwUr44vnJXVQJfXzuZCL8FAUM9IqZCqlZBgaWMbRw6JQ09xlF9s130Syzt1trfbZCC1jxbM4IHtPqxVXRg6DB11rsDheteFCtLuXHqJWTXqHkz4gMV7QZBRATgucFmF2ywZDZD",
  "2294459164144169": "EAAeeVSYcYQYBAOVAMY6T8t6htQMnJ3gGZBfq9H7VsvRaazNsqJ6FIfsIYK2GBAWRNrFzyB95BADbeZBZClDP6Vdf7Jp7gtpYIIur4oPZCBl4VXpAf3P4kjM8ldR3heOXbUZCFBzvk6rfB0iTPOlqhSKUySb8afVp8rLNnBMR1O0E71D1vfOlvAu3g0lvGRAkZD",
  "107410281020965": "EAAEPUuhsrWoBAHxawN6gux95MsTYmTZCFIrv1EZCufcmcF69XFkZAckyJMZBi23We79Kca00kMY6WiVKb8qZBQewZCWW3M0waSScEHNZBIAaz1jIT2ureHD6RDnRuyV8h9ZB9L7ZC0gSikJw3k2EGvDgspZB4sbiZC6k2WeGoZBeWd2MNUD1RTuN0OjqnTUuiWQXq6AZD",
  "1706997962917259":"EAAYSP5VrZCGsBACqCHZCiDn37gjF0j8R2KwaZADBpZChXKdvg9wNCJAegN7Q1n8VfwZAe5sICQKz9wHpidDq4VbmFVh7mmMFeAZBqQQvAQtq20TQZB94AvE2jQau3BRGqj64F1tCBFPneIS699IOzGPlhaRyxOmxYVZCVmcUg1f08VXjdMfpBpLMCzvdDZAjLUWAZD",
  "536242893451092": "EAAYSP5VrZCGsBALiPqTnIBtZACGSCoo4wrpsOh2aZBHFZBVnwuDHoLC5LDZB3yjCfLwWqKn2DRtYeXjtz0sVZBvhZAfCk5ipiSZCkOUEQ3IfPgpIab8vOnPGMJosZAINUhfrJr1qVxZAcqCVaqIHv0AH0gN453mZCkobpRxXbKHUZAvgX5046ZAYGfwjPz0W0JjV0EQoZD"
}

SEND_API_URL = 'https://graph.facebook.com/v6.0/me/messages?access_token=%s'\

PASS_THREAD_CONTROL_URL = 'https://graph.facebook.com/v2.12/me/pass_thread_control?access_token=%s'\
  % PAGE_ACCESS_TOKEN

TAKE_THREAD_CONTROL_URL = 'https://graph.facebook.com/v2.12/me/take_thread_control?access_token=%s'\
% PAGE_ACCESS_TOKEN

HEADERS = {'content-type': 'application/json'}

PAGE_INBOX = 263902037430900

ME = '620697518375534'

def send_message(body):
  print('send_message')
  print(body)
  try:
    for entry in body['entry']:
        if 'messaging' in entry:
          channel = 'messaging'
        else:
          channel = 'standby'
        for message in entry[channel]:
          sender = message['sender']['id']
          recipient_id =  message['recipient']['id']
          
          if 'message' in message: 
            webhook_type='message'
          elif 'postback' in message:
            webhook_type='postback'
          elif 'reaction' in message:
            webhook_type='reaction'
          else:
            return
          if 'text' in message[webhook_type]:
            msg_text = message[webhook_type]['text']
            if 'echoing_back' in msg_text:
              return
          body['echoing_back'] = 'true'
          print('sender1111')
          if 'is_echo' in message[webhook_type]:
            send_message_to_recipient(json.dumps(body), recipient_id, sender)
          else:
            send_message_to_recipient(json.dumps(body), sender, recipient_id)
          print('sender')
          print(sender)
          return
    print('sender')
  except Exception as e:
     print("swapnilc-Exception sending")
     print(e)
      
      
def send_message_to_recipient(message_text, recipient_id, page_id):
  message = {
    'recipient': {
      'id': recipient_id,
    },
    'message': {
      'text': message_text,
    },
  }
  r = requests.post(SEND_API_URL%PATs[page_id], data=json.dumps(message), headers=HEADERS)
  if r.status_code != 200:
    print('== ERROR====')
    print(SEND_API_URL)
    print(r.json())
    print('==============')

def pass_thread_control(app_id, recipient_id):
  payload = {
    'recipient': {
      'id': recipient_id,
    },
    'target_app_id': app_id,
  }
  r = requests.post(PASS_THREAD_CONTROL_URL, data=json.dumps(payload), headers=HEADERS)
  if r.status_code != 200:
    print('====ERROR====')
    print(r.json())
    print(r.request.data)
    print('==============')

def take_thread_control(recipient_id):
  payload = {
    'recipient': {
      'id': recipient_id,
    },
  }
  r = requests.post(TAKE_THREAD_CONTROL_URL, data=json.dumps(payload), headers=HEADERS)
  if r.status_code != 200:
    print('====ERROR====')
    print(r.json())
    print(r.request.data)
    print('==============')

def pass_thread_control_to_page_inbox(recipient_id):
  pass_thread_control(PAGE_INBOX, recipient_id)

def handle_messaging_event(message):
  sender = message['sender']['id']
  if sender == ME:
    return

  if 'request_thread_control' in message:
    send_message_to_recipient('Transferring you to live agent.', sender)
    pass_thread_control(message['request_thread_control']['requested_owner_app_id'], sender)
    return

  if 'message' not in message:
    return
  if 'text' not in message['message']:
    return
  message_text = message['message']['text']
  if 'return policy' in message_text:
    send_message_to_recipient('We offer full refunds up to 30 days, with a valid receipt.', sender)
  elif 'address' in message_text:
    send_message_to_recipient('You can find us at 123 Hacker Way, Menlo Park, CA 94025.', sender)
  elif 'hours' in message_text:
    send_message_to_recipient('We\'re open 9:00 AM - 5:30 PM from Monday to Saturday.', sender)
  else:
    send_message_to_recipient('I\'m sorry, I am not able to help with that. I\'ll transfer you over to a live agent.', sender)
    pass_thread_control_to_page_inbox(sender)

def handle_standby_event(standby_event):
  if 'sender' not in standby_event:
    return
  if 'id' not in standby_event['sender']:
    return
  sender = standby_event['sender']['id']
  if 'message' not in standby_event:
    return
  if 'text' not in standby_event['message']:
    return
  message_text = standby_event['message']['text']
  if 'deliver' in message_text:
    take_thread_control(sender)
    send_message_to_recipient('I noticed you asking about delivery options. Let me redirect you to our automated delivery processing service.', sender)

def handle_entry(entry):
  if 'messaging' in entry:
    for message in entry['messaging']:
      handle_messaging_event(message)
  elif 'standby' in entry:
    for standby_event in entry['standby']:
      handle_standby_event(standby_event)

@app.route('/')
@app.route('/index')
def index():
  return 'Hello, World!'

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
  if request.method == 'GET':
    mode = request.args['hub.mode']
    token = request.args['hub.verify_token']
    challenge = request.args['hub.challenge']
    if mode and token:
      if mode == 'subscribe' and token == WEBHOOK_VERIFY_TOKEN:
        return challenge
      else:
        return make_response('wrong token', 403)
    else:
      return make_response('invalid params', 400)
  else: # POST
    body = json.loads(request.data)
    print("swapnilc-Mydata")
    print(body)
    send_message(body)
    return ("", 205)

