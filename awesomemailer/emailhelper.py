import importlib


class EmailSender:
  def __init__(self, dataHandler, providers, importer=importlib):
    """
    Arguments:
    dataHandler -- a dataHandler containing the email data

    Keyword arguments:
    importer -- a module or class which can import at module given
      its name as a string (default: importlib).
    """
    self.dataHandler = dataHandler
    self.providers = providers
    self.importer = importer
    self.providerInfo = {}


  def getProviderInfo(self, name=None):
    """
    Convenience accessor method for the provider info dict
    Returns None if there is no provider info or the name
    given is not present in the dict. If no name is given,
    the complete dict is returned.

    Keyword arguments:
    name -- the name of a specific provider (default: None).

    Return:
    The complete providerInfo dict is returned if name is None,
    otherwise, only the data associated with the key `name` is
    returned (or None if the key does not exist).
    """
    if name is None:
      return self.providerInfo
    else:
      return self.providerInfo.get(name, None)


  def send(self):
    """
    Sends emails using the providers. If a provider fails to 
    send all the emails, the next provider in the list is used
    to send the remaining emails. 

    Return:
    A dict containing some successfully sent emails, as well as 
    those failed.
    """
    successList = []

    remainingReceivers = self.dataHandler.receivers
    for providerName, apiKey in self.providers:
      # Import the provider
      provider = self.importer.import_module(providerName)

      # Prepare data for the email providers
      data = {
        'from'    : self.dataHandler.sender,
        'to'      : remainingReceivers,
        'subject' : self.dataHandler.subject,
        'message' : self.dataHandler.message
      }

      # Send emails using provider
      res = provider.send(data, apiKey)

      # Update successful and pending email lists
      successList.extend(res['successes'])
      remainingReceivers = [obj['mail'] for obj in res['errors']]

      # Update provider info
      self.providerInfo[providerName] = self.providerInfo.get(providerName, {'successes': 0, 'errors': 0})
      self.providerInfo[providerName]['successes'] += len(res['successes'])
      self.providerInfo[providerName]['errors'] += len(res['errors'])

      # Break if all mails are sent
      if not res['errors']:
        break

    return {'successes': successList, 'errors': remainingReceivers}
