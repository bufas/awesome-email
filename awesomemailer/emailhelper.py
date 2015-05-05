import importlib
from validate_email import validate_email


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
      self.dataHandler.receivers = remainingReceivers

      # Send emails using provider
      res = provider.send(self.dataHandler, apiKey)

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


class EmailDataHandler:
  def __init__(self, sender, receivers, subject, message):
    self.sender    = sender
    self.receivers = receivers
    self.subject   = subject
    self.message   = message

    self._sanitize()


  def _sanitize(self):
    """
    Sanitizes the data by stripping whitespace and adding missing
    values.
    """
    self.sender = self.sender.strip()

    self.receivers = self.receivers.strip()
    if self.receivers == '':
      self.receivers = []
    else:
      self.receivers = self.receivers.split(',')

    self.subject = self.subject.strip()

    self.message = self.message.strip()
    if self.message == '':
      self.message = ' '  # The providers can not send empty emails


  def getReceiversAsString(self):
    """Returns the reciver list as a comma separated string"""
    return ','.join(self.receivers)


  def getErrors(self):
    """
    Searches the data for errors. If no errors are detected, 
    None is returned. If one or more errors are detected, a list
    of errors are returned
    """
    def addError(errors, name, err):
      tmp = errors.get(name, list())
      tmp.append(err)
      errors[name] = tmp

    errors = dict()

    if not self.sender:
      addError(errors, 'sender', 'Required')

    if not self.receivers:
      addError(errors, 'receivers', 'Required')

    if not errors.get('sender', []) and not validate_email(self.sender):
      addError(errors, 'sender', 'Invalid email')

    for receiver in self.receivers:
      if not validate_email(receiver):
        addError(errors, 'receivers', {'email': receiver, 'reason': 'Invalid email'})

    if errors:
      return errors
    else:
      return None
