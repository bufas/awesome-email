import mandrill
import requests

"""
Sends emails using the Mandrill service.
https://mandrillapp.com
"""

def send(data, apiKey=None):
  """See __init__.py for documentation"""
  acceptedStatuses = ['sent', 'queued', 'scheduled']

  successMails = []
  errorMails = []

  try:
    mandrill_client = mandrill.Mandrill(apiKey)

    message = dict({'from_email' : data.sender,
                    'subject'    : data.subject,
                    'text'       : data.message,
                    'to'         : [{'email' : mail} for mail in data.receivers]})

    result = mandrill_client.messages.send(message=message)

    successMails = [r['email'] for r in result if r['status'] in acceptedStatuses]
    errorMails = [{'mail' : r['email'], 'reason' : r['reject_reason']} 
                  for r in result if r['status'] not in acceptedStatuses]

  except mandrill.Error as e:
    errorMails = [{'mail' : mail, 'reason' : str(e)} for mail in data.receivers]
  except requests.exceptions.ConnectionError as e:
    errorMails = [{'mail' : mail, 'reason' : 'ConnectionError'} for mail in data.receivers]

  return {'successes' : successMails, 'errors' : errorMails}
