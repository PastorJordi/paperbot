import slack 
from flask import Flask
from slackeventsapi import SlackEventAdapter
import os
from download_example import download_by_doi
import threading
import urllib.request
# so the issue is that it runs slow...https://github.com/slackapi/python-slack-sdk/issues/801
# try running it in a thread so perhaps we avoid duplicates issue
# template copy-pasted from this guy # https://www.youtube.com/watch?v=6gHvqXrfjuo

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(
    os.environ.get('SLACK_SIGNING_SECRET'),
    '/slack/events', 
    app
)

external_ip = None

client = slack.WebClient(token=os.environ['SLACK_BOT_TOKEN'])
#client.chat_postMessage(channel='#testbots', text='pre-connected')
BOT_ID = client.api_call('auth.test')['user_id']
#client.chat_postMessage(channel='#testbots', text=f'bot id = {BOT_ID}')

def refined_doi(event,words):
    _, _, doi = words
    wheretopost = event.get('channel')
    ret, pth = download_by_doi(doi)
    if ret:
        client.files_upload(channels=wheretopost, file=pth, initial_comment='I hope is this one')
        os.remove(pth)
    else:
        client.chat_postMessage(
                        channel=wheretopost,
                        text=f"something went wrong when retrieving the paper by doi> here's the traceback\n{pth}")

def sendip(event, words):
    global external_ip
    if external_ip is None:
        external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')

    wheretopost = event.get('user')
    try:
        client.chat_postMessage(
                        channel=wheretopost,
                        text=f"{external_ip}")
    except Exception as e:
        client.chat_postMessage(
                        channel=wheretopost,
                        text=f"something went wrong when executing function sendip .here's the traceback\n{e}")

#def send_help():
#    helpstr = 'by now this just works with @mention doi [doistring]'

funs = {
    #'help' : send_help
    'doi' : refined_doi,
    'ip': sendip
}

@slack_event_adapter.on('app_mention')
def handle_msg(payload):
    event = payload.get('event', {})
    #channel_id = event.get('channel')
    user_id = event.get('user')
    text= event.get('text')
    words = text.split()
    
    try:
        th = threading.Thread(target=funs[words[1]], args=(event,words), daemon=True)
        th.start()
        # funs[words[1]](channel_id,words[2]) # first one is mention
    except Exception as e: 
        client.chat_postMessage(channel=user_id, text=f'did not understand {words[1]} or there was an uncaught exception\n {repr(e)}')
    # if user_id!=BOT_ID:
    #     client.chat_postMessage(channel=channel_id, text='message aknowledged\n'+text)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') # add port=int
