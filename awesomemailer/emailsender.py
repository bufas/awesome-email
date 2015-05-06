import importlib


class EmailSender:
  def __init__(self, dataHandler, providers, importer=importlib, logger=None):
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
    self.logger = logger


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

    self.log('Sending to {}'.format(','.join(self.dataHandler.receivers)))

    remainingReceivers = self.dataHandler.receivers
    for providerModel in self.providers:
      providerName = providerModel.name

      self.log('Trying provider {}'.format(providerName))

      # Import the provider
      provider = self.importer.import_module(providerName)

      # Prepare data for the email providers
      self.dataHandler.receivers = remainingReceivers

      # Send emails using provider
      res = provider.send(self.dataHandler, providerModel.key)

      # Update successful and pending email lists
      successList.extend(res['successes'])
      remainingReceivers = [obj['mail'] for obj in res['errors']]

      # Update provider info
      self.providerInfo[providerName] = self.providerInfo.get(providerName, {'successes': 0, 'errors': 0})
      self.providerInfo[providerName]['successes'] += len(res['successes'])
      self.providerInfo[providerName]['errors'] += len(res['errors'])

      # Log
      if not res['successes']:
        self.log('Complete failure no email sent')
      else:
        if res['errors']:
          self.log('Successfully sent to {}'.format(','.join(res['successes'])))
          for err in res['errors']:
            self.log('Failed to send to {} : {}'.format(err['mail'], err['reason']))
        else:
          self.log('Successfully sent to all')

      # Break if all mails are sent
      if not res['errors']:
        break

    # More logging
    if not remainingReceivers:
      self.log('All emails sent')
    else:
      self.logger.info('success/failure = {}/{}'.format(len(successList), len(remainingReceivers)))

    return {'successes': successList, 'errors': remainingReceivers}


  def log(self, msg):
    if self.logger is not None:
      self.logger.info('[EmailSender] {}'.format(msg))
