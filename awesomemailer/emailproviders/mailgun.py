import requests

"""
Sends emails using the Mailgun service.
https://mailgun.com
"""

def send(data, apiKey=None):
  """See __init__.py for documentation"""
  successList = []
  errorList = []

  try:
    res = requests.post(
      'https://api.mailgun.net/v3/sandbox96a16a12ead7492e950f30e4a2feb1fa.mailgun.org/messages',
      auth=('api', apiKey),
      data={'from'    : data.sender,
            'to'      : data.getReceiversAsString(),
            'subject' : data.subject,
            'text'    : data.message})

    if res.status_code == 200:
      successList = data.receivers
    else:
      errorList = [{'mail' : mail, 'reason' : res.reason} for mail in data.receivers]
  except requests.exceptions.ConnectionError as e:
    errorList = [{'mail' : mail, 'reason' : 'ConnectionError'} for mail in data.receivers]

  return {'successes' : successList, 'errors' : errorList}
