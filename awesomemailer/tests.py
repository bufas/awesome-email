# import mailer
import unittest
from mock import Mock
import json
import validation

import utils

class ValidationTestCase(unittest.TestCase):
  def setUp(self):
    self.mail1 = 'email@example.com'
    self.mail2 = 'my.name@domain.eu'
    self.mail3 = 'wat7900@aroundtheworld.org'
    self.invalidMail1 = 'noathere.com'
    self.invalidMail2 = 'asdf'

  
  def tearDown(self):
    pass


  def test_validateValidSingleTo(self):
    data = {'from' : self.mail1, 'to' : [self.mail1], 'subject' : '', 'message' : ''}
    self.assertIsNone(validation.isValid(data))


  def test_validateValidMultipleTo(self):
    data = {'from' : self.mail1, 
            'to' : [self.mail1, self.mail2, self.mail3], 
            'subject' : '', 
            'message' : ''}
    self.assertIsNone(validation.isValid(data))


  def test_validateInvalidEmptyFrom(self):
    data = {'from' : '', 'to' : [self.mail1], 'subject' : '', 'message' : ''}
    res = validation.isValid(data)
    self.assertTrue('Required' in res['from'])


  def test_validateInvalidEmptyTo(self):
    data = {'from' : 'from_email@example.com', 'to' : [], 'subject' : '', 'message' : ''}
    res = validation.isValid(data)
    self.assertTrue('Required' in res['to'])


  def test_validateInvalidInvalidFrom(self):
    data = {'from' : self.invalidMail1, 'to' : [self.mail1], 'subject' : '', 'message' : ''}
    res = validation.isValid(data)
    self.assertTrue('Invalid email' in res['from'])


  def test_validateInvalidInvalidToAll(self):
    data = {'from' : self.mail1, 
            'to' : [self.invalidMail1, self.invalidMail2], 
            'subject' : '', 
            'message' : ''}
    res = validation.isValid(data)
    self.assertEqual(len(res['to']), 2)
    self.assertEqual(res['to'][0]['email'], self.invalidMail1)
    self.assertEqual(res['to'][0]['reason'], 'Invalid email')
    self.assertEqual(res['to'][1]['email'], self.invalidMail2)
    self.assertEqual(res['to'][1]['reason'], 'Invalid email')


  def test_validateInvalidInvalidToSubset(self):
    data = {'from' : self.mail1, 
            'to' : [self.invalidMail1, self.mail1], 
            'subject' : '', 
            'message' : ''}
    res = validation.isValid(data)
    self.assertEqual(len(res['to']), 1)
    self.assertEqual(res['to'][0]['email'], self.invalidMail1)
    self.assertEqual(res['to'][0]['reason'], 'Invalid email')


class SanitizerTestCase(unittest.TestCase):
  def setUp(self):
    pass


  def tearDown(self):
    pass


  def test_sanitizeTooFewArgs(self):
    res = validation.sanitize({})
    self.assertTrue('from' in res)
    self.assertTrue('to' in res)
    self.assertTrue('subject' in res)
    self.assertTrue('message' in res)


  def test_sanitizeEmptyListForTo(self):
    res = validation.sanitize({})
    self.assertTrue(type(res['to']) is list)
    self.assertEqual(len(res['to']), 0)


class EmailSenderTestCase(unittest.TestCase):
  def setUp(self):
    pass


  def tearDown(self):
    pass


  def makeProviderMock(self, sendReturn):
    mock = Mock()
    mock.send = Mock(return_value=sendReturn)
    return mock


  def makeImporterMock(self, providerMocks):
    mock = utils.CustomProviderImporter()
    mock.import_module = Mock(side_effect=providerMocks)
    return mock


  def test_singleProvider(self):
    data = {'from': 'a@b.com', 'to': ['c@d.com', 'e@f.com'], 'subject': '', 'message': ' '}
    providerreturn = {'successes': ['c@d.com', 'e@f.com'], 'errors': []}

    mockprovider = self.makeProviderMock(providerreturn)
    mockimporter = self.makeImporterMock([mockprovider])

    res = utils.sendEmails(data, [('name', 'key')], mockimporter)

    self.assertEquals(len(res['successes']), 2)
    self.assertEquals(len(res['errors']), 0)


  def test_onlyUsedProvidersAreLoaded(self):
    data = {'from': 'a@b.com', 'to': ['c@d.com', 'e@f.com'], 'subject': '', 'message': ' '}
    providerreturn = {'successes': ['c@d.com', 'e@f.com'], 'errors': []}

    mockprovider = self.makeProviderMock(providerreturn)
    mockimporter = self.makeImporterMock([mockprovider])

    res = utils.sendEmails(data, [('name1', 'key'), ('name2', 'key')], mockimporter)

    self.assertEquals(len(res['successes']), 2)


  def test_whenFirstProviderFailsTheSecondKicksIn(self):
    data = {'from': 'a@b.com', 'to': ['c@d.com', 'e@f.com'], 'subject': '', 'message': ' '}
    providerreturn1 = {'successes':[], 
                       'errors':[{'mail':'c@d.com','reason':''}, {'mail':'e@f.com','reason':''}]}
    providerreturn2 = {'successes':['c@d.com', 'e@f.com'], 'errors':[]}

    mockprovider1 = self.makeProviderMock(providerreturn1)
    mockprovider2 = self.makeProviderMock(providerreturn2)
    mockimporter = self.makeImporterMock([mockprovider1, mockprovider2])

    res = utils.sendEmails(data, [('name1', 'key'), ('name2', 'key')], mockimporter)

    self.assertEquals(res['senders'][0]['errors'], 2)
    self.assertEquals(res['senders'][1]['successes'], 2)


  def test_sendEmailMultipleProvidersFirstFailsSome(self):
    data = {'from': 'a@b.com', 'to': ['c@d.com', 'e@f.com', 'g@h.com'], 'subject': '', 'message': ' '}
    providerreturn1 = {'successes':['c@d.com'], 
                       'errors':[{'mail':'e@f.com','reason':''}, {'mail':'g@h.com','reason':''}]}
    providerreturn2 = {'successes':['e@f.com', 'g@h.com'], 'errors':[]}

    mockprovider1 = self.makeProviderMock(providerreturn1)
    mockprovider2 = self.makeProviderMock(providerreturn2)
    mockimporter = self.makeImporterMock([mockprovider1, mockprovider2])

    res = utils.sendEmails(data, [('name1', 'key'), ('name2', 'key')], mockimporter)

    self.assertEquals(res['senders'][0]['successes'], 1)
    self.assertEquals(res['senders'][0]['errors'], 2)
    self.assertEquals(res['senders'][1]['successes'], 2)
    self.assertEquals(res['senders'][1]['errors'], 0)


class ProviderImporterTestCase(unittest.TestCase):
  def setUp(self):
    pass


  def tearDown(self):
    pass


  def test_customProviderImporter(self):
    importer = utils.CustomProviderImporter()
    provider = importer.import_module('emailproviders.mailgun')
    self.assertTrue(hasattr(provider, 'send'))


# class AwesomeMailerTestCase(unittest.TestCase):
  # def setUp(self):
  #   mailer.app.config.from_object('config_test');
  #   self.app = mailer.app.test_client()

  #   self.providerMandrill = ('mandrillsender', MANDRILL_API_KEY)
  #   self.providerMailgun = ('mailgunsender', MAILGUN_API_KEY)

  # Test the mailgun adapter

  # Test the mandrill adapter

  # def test_mandrillSendMail(self):
  #   emailData = dict({
  #     'EMAIL_FROM'    : 'from_email@example.com',
  #     'EMAIL_TO'      : 'to_email@example.com',
  #     'EMAIL_SUBJECT' : 'Ny post i din eboks',
  #     'EMAIL_MESSAGE' : 'Ligegyldigt indhold'
  #   })

  #   rv = self.app.post('/send_mail', data=emailData)
  #   realData = json.loads(rv.data)
  #   print rv.data
  #   # assert 'status' in realData and realData['status'].startswith('sent')
  #   # realData['status'].startswith('Queued')

if __name__ == '__main__':
  unittest.main()