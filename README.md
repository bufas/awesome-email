Uber coding challenge
=====================

[![Build Status](https://travis-ci.org/bufas/awesome-email.svg?branch=master)](https://travis-ci.org/bufas/awesome-email)

Exercise spec can be found [here](https://github.com/uber/coding-challenge-tools/blob/master/coding_challenge.md)

Email service provider
----------------------
An email service provider adapter must expose a single function `send()` that takes two arguments, namely the email data (e.g. from address, to address, subject, etc.) and an API key. It must return a dictionary containing the two keys `successes` and `errors`. `successes` must be a list of addresses to which the email was sent successfully, and `errors` must be a list of dictionaries each containing the email address that failed along with a reason.

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