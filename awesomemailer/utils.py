from validate_email import validate_email
import importlib

class CustomProviderImporter:
  """
  Imports email providers and returns them. It has the same interface
  as importlib, which means importlib can simply be used in its place.
  This is mainly for testing.
  """
  def __init__(self):
    self.importedProviders = {}

  def import_module(self, providerName):
    # If the provider has been loaded before, just return it
    if providerName in self.importedProviders:
      return self.importedProviders[providerName]

    # Load the provider
    provider = importlib.import_module(providerName)
    self.importedProviders[providerName] = provider
    return provider

def sendEmails(data, providers, importer=importlib):
  successfulSends = []
  remainingReceivers = data['to']
  senderInformation = []

  for providerName, apiKey in providers:
    provider = importer.import_module(providerName)                  # Import the adapter
    sendRes = provider.send(data, apiKey)                            # Try to send emails
    successfulSends.extend(sendRes['successes'])                     # Update successful sends
    remainingReceivers = [obj['mail'] for obj in sendRes['errors']]  # Update remaining emails
    data['to'] = remainingReceivers
    senderInformation.append({'provider'  : providerName,            # Store info about this provider
                              'successes' : len(sendRes['successes']),
                              'errors'    : len(sendRes['errors'])})
    if not sendRes['errors']:
      break                                                          # Break if there are no errors

  return {'successes' : successfulSends, 
          'errors'    : remainingReceivers,
          'senders'   : senderInformation}

def sanitize(data):
  clean = dict()
  clean['from'] = data.get('from', '').strip()
  tmpTo = data.get('to', '').strip()
  clean['to'] = [] if tmpTo == '' else tmpTo.split(',')
  clean['subject'] = data.get('subject', '')
  clean['message'] = data.get('message', '')
  clean['message'] = ' ' if clean['message'] == '' else clean['message']
  return clean

def isValid(data):
  anyErrors = False
  error = {'from' : [], 'to' : [], 'subject' : [], 'message' : []}
  requiredFields = ['from', 'to']

  # Check if required fields are filled out
  for field in requiredFields:
    if not data[field]:
      error[field].append('Required')
      anyErrors = True

  # Validate the 'from' address
  if len(error['from']) == 0 and not validate_email(data['from']):
    error['from'].append('Invalid email')
    anyErrors = True

  # Validate the 'to' addresses
  for email in data['to']:
    if not validate_email(email):
      error['to'].append({'email' : email, 'reason' : 'Invalid email'})
      anyErrors = True

  if anyErrors:
    return error

  return None
