import requests

"""
Sends emails using the Mailgun service.
https://mailgun.com
"""

def send(data, apiKey=None):
  """See __init__.py for documentation"""
  receiverString = ','.join(data['to'])

  successList = []
  errorList = []

  try:
    res = requests.post(
      'https://api.mailgun.net/v3/sandbox96a16a12ead7492e950f30e4a2feb1fa.mailgun.org/messages',
      auth=('api', apiKey),
      data={'from'    : data['from'],
            'to'      : receiverString,
            'subject' : data['subject'],
            'text'    : data['message']})

    if res.status_code == 200:
      successList = data['to']
    else:
      errorList = [{'mail' : mail, 'reason' : res.reason} for mail in data['to']]
  except requests.exceptions.ConnectionError as e:
    errorList = [{'mail' : mail, 'reason' : 'ConnectionError'} for mail in data['to']]

  return {'successes' : successList, 'errors' : errorList}
