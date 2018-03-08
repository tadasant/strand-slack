# Strand Slack

[![CodeFactor](https://www.codefactor.io/repository/github/solutionloft/code-clippy-slack/badge)](https://www.codefactor.io/repository/github/solutionloft/code-clippy-slack)

## Getting Started
To start, clone the repository locally and create a virtual environment. Install the dependencies from the requirements file into your virtual environment.

## Running Tests
If you're using PyCharm, simply use the "Run Tests" run configuration to run all the tests.

Without PyCharm, `cd` into the root directory and run `pytest --flake8 --pep8 --no-cov`

You can also run `ptw` to run pytest-watch

## Running the application
Note that you'll need strand-api running on `CORE_API_HOST`

Make sure you've created a superuser with username `ccs`, email `ccs@solutionloft.com` and password `randomPassword`.

`$ python manage.py createsuperuser --username ccs`.

If you're using PyCharm, simply use the "Run (Local)" run configuration to start the Flask server.

If not, `cd` into the root directory and run `python3 run.py`


## Using ngrok for development
ngrok sets up a tunnel online so that we have an external URL to tell Slack about.

This is useful because much of strand-slack relies on triggers from Slack callbacks over the wire.

Steps to use ngrok:
1) Download ngrok, unzip, and put the script somewhere in your $PATH (likely `/usr/bin/local`)
2) Run `ngrok http 5000` (assuming 5000 is the `PORT` you set in `development.config.json`)
3) You can watch the requests getting routed through the tunnel at <http://localhost:4040/inspect/http>
4) Take the forwarding address (e.g. <http://5c80fc28.ngrok.io>) and configure it on <https://api.slack.com/apps/A8YTKNNMQ/interactive-messages>

Now Slack will be able to call your local server as you interact with the app!

Note that on the free ngrok plan, you'll need to do this every time you restart ngrok.
