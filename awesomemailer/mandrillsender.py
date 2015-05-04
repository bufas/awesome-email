import mandrill

def send(data, apiKey=None):
  acceptedStatuses = ['sent', 'queued', 'scheduled']

  try:
    mandrill_client = mandrill.Mandrill(apiKey)

    message = dict({'from_email' : data['from'],
                    'subject'    : data['subject'],
                    'text'       : data['message'],
                    'to'         : [{'email' : mail} for mail in data['to']]})

    result = mandrill_client.messages.send(message=message)

    successMails = [r['email'] for r in result if r['status'] in acceptedStatuses]
    errorMails = [{'mail' : r['email'], 'reason' : r['reject_reason']} 
                  for r in result if r['status'] not in acceptedStatuses]
                  
    return {'successes' : successMails, 'errors' : errorMails}

  except mandrill.Error as e:
    errorMails = [{'mail' : mail, 'reason' : str(e)} for mail in data['to']]
    return {'successes' : [], 'errors' : errorMails}
