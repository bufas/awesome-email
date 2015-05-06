Awesome email sending webpage
=============================

[![Build Status](https://travis-ci.org/bufas/awesome-email.svg?branch=master)](https://travis-ci.org/bufas/awesome-email)

Demo
----
A demo has been set up on Heroku [https://tranquil-lowlands-1979.herokuapp.com/](https://tranquil-lowlands-1979.herokuapp.com/)

What is this?
-------------
A website that can send emails. The frontend is extremely simple. It takes the input needed to send an email, and posts it to the server. Some validation is also done when the submit button is clicked, but not a lot has gone into making it pretty (obviously).

The backend is more interesting. It is written in Python, and uses the [Flask web framework](http://flask.pocoo.org/). Other than serving static resources it handles the data posted from the form by sending out emails according to the data. Emails are sent using one or more email service providers. Currently, only two providers are included, namely Mandrill and Mailgun, but more can easily be added. If one provider fails, another one will take over and send the remaining emails until all emails have been sent or all providers have failed. The providers are tried in the order of their rank in the database. This logic should probably be cleverer so that a provider that fails every time is not always tried first.

Running the system
------------------
- Install dependencies by running `pip install -r requirements.txt`.
- Create a postgres database
- Set the `DATABASE_URL` environment variable to the postgres connection URI string (postgresql://user:password@host/database). The environment variables can also be set using the `.env` file (foreman will automatically set the environment before launching the server).
- Insert the desired email service providers into the database (A script should probably be made for this).
- Cross your fingers, hope that you have set it up correctly, and run `foreman start web`. This will start a [gunicorn](http://gunicorn.org/) web server.

If you wish to run the tests, your environment will need need to contain the following variables
- TESTING=True
- MANDRILL_API_KEY_TEST=[Mandrill API key]
- MAILGUN_API_KEY_TEST=[Mailgun API key]

If I had an infinite amount of time
-----------------------------------
- I would implement som more email service providers
- I would store more data about the performance of the email service providers to make a better decision about the order in which providers are tried.
- I would implement a small control panel where email service providers can be managed (enabled/disabled) and inspected (number of successes/errors).
- I would set up webhooks to get notified when emails are received/bounced/opened/clicked/etc. and notify the user. [Firebase](https://www.firebase.com/) would probably be an awesome mechanism as the server-to-user notification system.
- I would set up a database migration method as it is kinda bad how it is now. Should probably be done with [Flask Migrate](https://flask-migrate.readthedocs.org/en/latest/).
- I would write more thorough tests for the email service providers. Also, I would like a single test suite that can be run against all the service providers one by one. This will also make it easier for people who want to write their own providers.

Email service provider interface
--------------------------------
It is relatively easy to implement an email service provider. It must expose a single function `send()` that takes two arguments, namely the email data (e.g. from address, to address, subject, etc.) and an API key. It must return a dictionary containing two keys, `successes` and `errors`. `successes` must be a list of addresses to which the email was sent successfully, and `errors` must be a list of dictionaries each containing the email address that failed along with a reason.

An example return dictionary
```python
{
  'successes' : ['me@bbc.com', 'you@host.org'],
  'errors' : [
    {'mail' : 'hold@up.you', 'reason' : 'Insufficient funds'},
    {'mail' : 'dont@send.me', 'reason' : 'Connection timed out'}
  ]
}
```

Remember to add it to the database.