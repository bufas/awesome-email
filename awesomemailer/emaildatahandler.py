from validate_email import validate_email


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
