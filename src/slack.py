"""
A Python 3.6 script that sends a message to a Slack
Channel using Incoming WebHooks. The script uses
APScheduler to schedule the message and requests
to post the message to the Slack Channel.

The script uses 1 environment variable that holds the
Incoming Webhooks URL:

    slackIncomingWebhookUrl

Specify the channel and text for the message in the
send_message() function. The channel is optional if
you wish to use the default channel specfied when
creating the Incoming Webhook.

    message = {
        "channel": "#general",
        "text": "A message."
    }

Choose the interval or date and time you wish to
send the message.

    @sched.scheduled_job('interval', minutes=1)

APScheduler is quite flexible so you may want to
read its documentation to understand the various
ways to schedule a job.abs

    http://apscheduler.readthedocs.io/en/latest/
"""

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
import datetime, os, requests
from pysondb import db
import random

slack_url = os.getenv('SLACK_INCOMING_URL')
slack_channel = os.getenv('SLACK_CHANNEL')
schedulder = BlockingScheduler()


def load_data():
    try:
        messages = db.getDb("donutsdb.json")
    except Exception as err:
        print("Error while hadnling database: {0}".format(err))
        raise

    return messages


def random_greeting():
    greetings = ["Hey @here! it's :bagel: time,", "Salut @here, it's :bagel: time,", "Heeeyy @here, it's me again, your favorite bot (:bagel:) ever,", "Hey @here! Are you reaaaaaaady :bagel: ,"]
    return random.choice(greetings)

def random_message():
    messages = load_data().getAll()
    message = random.choice(messages)

    if message["used"] == True:
        random_message()
    else:
        delete_message(message)

    return message

def delete_message(message: object):
    id = message["id"]
    print(id)
    messages = db.getDb("donutsdb.json")
    messages.updateById(str(id), {"used": True})

def clean_message():
    msg_object = random_message()
    greeting = random_greeting()
    message = {
        "text": greeting + "\n>"+ msg_object['short_message'],
        "image": msg_object['image_url']
    } 
    return message

@schedulder.scheduled_job('cron', hour=21, minute=46, start_date='2021-02-21', end_date='2021-02-22', timezone='Europe/Paris')
def bot_introduction():
    message = {
        "channel": slack_channel,
        "text": "Hey WOOP, Please, let me introduce myself,\nMy name is Bagel :bagel:, i'am here to replace `donuts`, if you asking why? because he's sucks and so expensive for a dumb bot  $$$ :money_with_wings: #fuck_donuts.\nFor the record, i'am developped by *Haithem SOUALA*, and the questions database was Hacked by *Hélène BAILLEUL* (someone should call the police :male_police_officer: :female_police_officer:, this girl is dangerous). \n My first mission will start in less than one minute,\n>I love you all, BISOUS :heart:"
    }

    try:
        results = requests.post(slack_url, json = message)
    except Exception as err:
        print("Error while sending message: {0}".format(err))
    
    response = {
        'date': str(datetime.datetime.now()),
        'message': message,
        'statusCode': results.status_code
    }

    return response


#@schedulder.scheduled_job('interval', minutes=1)
@schedulder.scheduled_job('cron', day_of_week='mon-fri', hour=16, minute=00, timezone='Europe/Paris')
def send_message():
    message = clean_message()
    
    text = message['text']
    image = message['image']
    
    blocks = [{"type": "section", "text": {"type": "mrkdwn" ,"text": text }}]

    if image:
        blocks.append({"type": "image","image_url": image, "alt_text": "image"})

    message = {
        "channel": slack_channel,
        "blocks": blocks
    }

    try:
        results = requests.post(slack_url, json = message)
    except Exception as err:
        print("Error while sending message: {0}".format(err))

    response = {
        'date': str(datetime.datetime.now()),
        'message': message,
        'statusCode': results.status_code
    }

    return response


def event_listener(event):
    print(event.retval)

#if __name__ == "__main__":
#    send_message()

print("Running...")
schedulder.add_listener(event_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
schedulder.start()
