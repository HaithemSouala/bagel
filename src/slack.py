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
    return random.choice(messages)

def clean_message():
    msg_object = random_message()
    message = {
        "text": random_greeting() + "\n>"+ msg_object['short_message'],
        "image": msg_object['image_url']
    } 
    return message

"""
{
	"blocks": [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Salut @here, it's :bagel: time,\n>Who is one person you admire and why?"
			}
		},
		{
			"type": "image",
			"image_url": "https://media.giphy.com/media/dyLZiU6Vg0tTASdX1x/giphy.gif",
			"alt_text": "marg"
		}
	]
}

"""
#@schedulder.scheduled_job('cron', day_of_week='mon-fri', hour=16, minute=00, timezone='Europe/Paris')
@schedulder.scheduled_job('interval', minutes=1)
def send_message():
    blocks = [{"type": "section", "text": {"type": "mrkdwn" ,"text": clean_message()['text'] }}]

    if clean_message()['image']:
        blocks.append({"type": "image","image_url": clean_message()['image'], "alt_text": "image"})

    message = {
        "channel": slack_channel,
        "blocks": blocks
    }
    print(message)
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
