import slack 
from flask import Flask
from slackeventsapi import SlackEventAdapter
import os

# copy pasted from this guy

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(
    os.environ.get('SLACK_SIGNING_SECRET'),
    '/slack/events', 
    app
)


client = slack.WebClient(token=os.environ['SLACK_BOT_TOKEN'])
client.chat_postMessage(channel='#testbots', text='pre-connected')
BOT_ID = client.api_call('auth.test')['user_id']
client.chat_postMessage(channel='#testbots', text=f'bot id = {BOT_ID}')
@slack_event_adapter.on('app_mention')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text= event.get('text')
    if user_id!=BOT_ID:
        client.chat_postMessage(channel=channel_id, text='message aknowledged\n'+text)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') # add port=int
