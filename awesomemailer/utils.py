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

def sendEmails(dataHandler, providers, importer=importlib):
  """
  Sends emails using the providers. If a provider fails to send 
  all the emails, the next provider in the list is used to send 
  the remaining emails. A dict containing some diagnostics is 
  returned to inform to caller of broken services.

  Arguments:
  dataHandler -- a dataHandler containing the email data
  providers -- a list of tuples containg the name of an email 
    providers and an API key.

  Keyword arguments:
  importer -- a module or class which can import at module given
    its name as a string (default: importlib).

  Return value:
  Returns a dict containing a list of emails which was 
  successfully sent to, a list of emails which failed, and a 
  list of which providers were used as well as how many emails 
  they successfully sent and failed.
  """
  successfulSends = []
  remainingReceivers = dataHandler.receivers
  senderInformation = []

  for providerName, apiKey in providers:
    provider = importer.import_module(providerName)                  # Import the adapter

    # Prepare data
    data = {
      'from': dataHandler.sender,
      'to': remainingReceivers,
      'subject': dataHandler.subject,
      'message': dataHandler.message
    }

    sendRes = provider.send(data, apiKey)                            # Try to send emails
    successfulSends.extend(sendRes['successes'])                     # Update successful sends
    remainingReceivers = [obj['mail'] for obj in sendRes['errors']]  # Update remaining emails
    senderInformation.append({'provider'  : providerName,            # Store info about this provider
                              'successes' : len(sendRes['successes']),
                              'errors'    : len(sendRes['errors'])})
    if not sendRes['errors']:
      break                                                          # Break if there are no errors

  return {'successes' : successfulSends, 
          'errors'    : remainingReceivers,
          'senders'   : senderInformation}

