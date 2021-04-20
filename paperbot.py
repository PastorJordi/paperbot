#import slack # not being used
from flask import Flask
from slackeventsapi import SlackEventAdapter
import os

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(
    os.environ.get('SLACK_SIGNING_SECRET'),
    '/slack/events', 
    app
)


if __name__ == '__main__':
    app.run(debug=True) # add port=int