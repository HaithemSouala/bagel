# Slack Scheduler

A Python 3.6 script that sends a message to a Slack Channel using Incoming WebHooks. The script uses `APScheduler` to schedule the message and `requests` to post the message to the Slack Channel.

## Slack Incoming WebHooks

The script assumes you have created a custom integration for Incoming WebHooks for your Slack Group and have an *Incoming Webhook URL* where you can send JSON payloads.

If not, you will need to log into your Slack Group and create a custom Incoming WebHook for use with this script.

## Environment Variables

The script reads 1 environment variable, called `SLACK_INCOMING_URL`, that should contain the URL of the Incoming WebHook.

```
SLACK_INCOMING_URL
```

```
export SLACK_INCOMING_URL="{your URL}"
```

## Getting Started

The best way to run the script is to clone the github repository. Once you clone the repository, it is best to create a virtual environment and `pip install` the requirements.

### Step 1: Clone the Repository

```
$ git clone https://github.com/davidhayden/slack-scheduler.git
```

### Step 2: Create Virtual Environment and Install Requirements

Change into the project directory, create a virtual environment, and `pip install` the requirements in the `requirements.txt` file.

```
$ cd slack-scheduler

$ python -m venv env
$ source env/bin/activate
$ (env) pip install -r requirements.txt
```

### Step 3: Set Environment Variable

You must set 1 environment variable containing the Incoming Webhook URL of your Slack Group. It is convenient to set this variable in `~/.bash_profile` so it gets set when you open a terminal window. However, you can set it at the bash prompt for testing.

```
$ (env) export SLACK_INCOMING_URL={your URL}
```

### Step 4: Specify Slack Channel and Message Text

Specify the channel and text for the message in the `send_message` function. You can exclude the channel if you wish to accept the default channel you specified when creating the Incoming WebHook.

```py
message = {
    "channel": "#general",
    "text": "A message."
}
```

### Step 5: Specify the Message Interval

APScheduler is quite flexible. Currently the script sends the message to the Slack Channel every minute. You will want to modify this according to your application needs.

```py
@sched.scheduled_job('interval', minutes=1)
```

Read APScheduler's documentation for more information on scheduling jobs.

http://apscheduler.readthedocs.io/en/latest/

## Step 6: Run the Script

Run the script from the command line. You can press CTRL+C anytime to interrupt the script and return to the command line.

```
$ (env) python slack.py

Running...
{'date': '2017-12-14 16:55:29.362473', 'message': {'channel': '#general', 'text': 'A message.'}, 'statusCode': 200}
{'date': '2017-12-14 16:56:29.100282', 'message': {'channel': '#general', 'text': 'A message.'}, 'statusCode': 200}
{'date': '2017-12-14 16:57:29.270187', 'message': {'channel': '#general', 'text': 'A message.'}, 'statusCode': 200}
```
