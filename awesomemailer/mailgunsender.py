import requests

def send(data, apiKey=None):
  if (apiKey is None):
    raise

  # Format receiver list
  data['to'] = ','.join(data['to'])

  return requests.post(
    'https://api.mailgun.net/v3/sandbox96a16a12ead7492e950f30e4a2feb1fa.mailgun.org/messages',
    auth=('api', apiKey),
    data={
      'from'    : data['from'],
      'to'      : data['to'],
      'subject' : data['subject'],
      'text'    : data['message']
    }
  ).json()