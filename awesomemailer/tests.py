import mailer
import unittest
from mock import Mock
import json

from emailhelper import EmailSender, EmailDataHandler

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
    dataHandler = EmailDataHandler(self.mail1, self.mail1, '', '')
    self.assertIsNone(dataHandler.getErrors())


  def test_validateValidMultipleTo(self):
    receivers = ','.join([self.mail1, self.mail2, self.mail3])
    dataHandler = EmailDataHandler(self.mail1, receivers, '', '')
    self.assertIsNone(dataHandler.getErrors())


  def test_validateInvalidEmptyFrom(self):
    dataHandler = EmailDataHandler('', self.mail1, '', '')
    res = dataHandler.getErrors()
    self.assertTrue('Required' in res['sender'])


  def test_validateInvalidEmptyTo(self):
    dataHandler = EmailDataHandler(self.mail1, '', '', '')
    res = dataHandler.getErrors()
    self.assertTrue('Required' in res['receivers'])


  def test_validateInvalidInvalidFrom(self):
    dataHandler = EmailDataHandler(self.invalidMail1, self.mail1, '', '')
    res = dataHandler.getErrors()
    self.assertTrue('Invalid email' in res['sender'])


  def test_validateInvalidInvalidToAll(self):
    receivers = ','.join([self.invalidMail1, self.invalidMail2])
    dataHandler = EmailDataHandler(self.mail1, receivers, '', '')
    res = dataHandler.getErrors()
    self.assertEqual(len(res['receivers']), 2)
    self.assertEqual(res['receivers'][0]['email'], self.invalidMail1)
    self.assertEqual(res['receivers'][0]['reason'], 'Invalid email')
    self.assertEqual(res['receivers'][1]['email'], self.invalidMail2)
    self.assertEqual(res['receivers'][1]['reason'], 'Invalid email')


  def test_validateInvalidInvalidToSubset(self):
    receivers = ','.join([self.invalidMail1, self.mail1])
    dataHandler = EmailDataHandler(self.mail1, receivers, '', '')
    res = dataHandler.getErrors()
    self.assertEqual(len(res['receivers']), 1)
    self.assertEqual(res['receivers'][0]['email'], self.invalidMail1)
    self.assertEqual(res['receivers'][0]['reason'], 'Invalid email')


class SanitizerTestCase(unittest.TestCase):
  def setUp(self):
    pass


  def tearDown(self):
    pass


  def test_sanitizeNoReceivers(self):
    dataHandler = EmailDataHandler('', '', '', '')
    self.assertTrue(type(dataHandler.receivers) is list)
    self.assertEqual(len(dataHandler.receivers), 0)


  def test_sanitizeMessageNotEmpty(self):
    dataHandler = EmailDataHandler('', '', '', '')
    self.assertFalse(not dataHandler.message)


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
    mock = Mock()
    mock.import_module = Mock(side_effect=providerMocks)
    return mock


  def test_singleProvider(self):
    receivers = ','.join(['c@d.com', 'e@f.com'])
    dataHandler = EmailDataHandler('a@b.com', receivers, '', '')
    providerreturn = {'successes': ['c@d.com', 'e@f.com'], 'errors': []}

    mockprovider = self.makeProviderMock(providerreturn)
    mockimporter = self.makeImporterMock([mockprovider])

    sender = EmailSender(dataHandler, [('name', 'key')], importer=mockimporter)
    res = sender.send()

    self.assertEquals(len(res['successes']), 2)
    self.assertEquals(len(res['errors']), 0)


  def test_onlyUsedProvidersAreLoaded(self):
    receivers = ','.join(['c@d.com', 'e@f.com'])
    dataHandler = EmailDataHandler('a@b.com', receivers, '', '')
    providerreturn = {'successes': ['c@d.com', 'e@f.com'], 'errors': []}

    mockprovider = self.makeProviderMock(providerreturn)
    mockimporter = self.makeImporterMock([mockprovider])

    sender = EmailSender(dataHandler, [('name1', 'key'), ('name2', 'key')], importer=mockimporter)
    res = sender.send()

    self.assertEquals(len(res['successes']), 2)


  def test_whenFirstProviderFailsTheSecondKicksIn(self):
    receivers = ','.join(['c@d.com', 'e@f.com'])
    dataHandler = EmailDataHandler('a@b.com', receivers, '', '')
    providerreturn1 = {'successes':[], 
                       'errors':[{'mail':'c@d.com','reason':''}, {'mail':'e@f.com','reason':''}]}
    providerreturn2 = {'successes':['c@d.com', 'e@f.com'], 'errors':[]}

    mockprovider1 = self.makeProviderMock(providerreturn1)
    mockprovider2 = self.makeProviderMock(providerreturn2)
    mockimporter = self.makeImporterMock([mockprovider1, mockprovider2])

    sender = EmailSender(dataHandler, [('name1', 'key'), ('name2', 'key')], importer=mockimporter)
    res = sender.send()

    self.assertEquals(sender.getProviderInfo(name='name1')['errors'], 2)
    self.assertEquals(sender.getProviderInfo(name='name2')['successes'], 2)


  def test_sendEmailMultipleProvidersFirstFailsSome(self):
    receivers = ','.join(['c@d.com', 'e@f.com', 'g@h.com'])
    dataHandler = EmailDataHandler('a@b.com', receivers, '', '')
    providerreturn1 = {'successes':['c@d.com'], 
                       'errors':[{'mail':'e@f.com','reason':''}, {'mail':'g@h.com','reason':''}]}
    providerreturn2 = {'successes':['e@f.com', 'g@h.com'], 'errors':[]}

    mockprovider1 = self.makeProviderMock(providerreturn1)
    mockprovider2 = self.makeProviderMock(providerreturn2)
    mockimporter = self.makeImporterMock([mockprovider1, mockprovider2])

    sender = EmailSender(dataHandler, [('name1', 'key'), ('name2', 'key')], importer=mockimporter)
    res = sender.send()

    provider1info = sender.getProviderInfo(name='name1')
    provider2info = sender.getProviderInfo(name='name2')
    self.assertEquals(provider1info['successes'], 1)
    self.assertEquals(provider1info['errors'], 2)
    self.assertEquals(provider2info['successes'], 2)
    self.assertEquals(provider2info['errors'], 0)


class AwesomemailerTestCase(unittest.TestCase):
  """Integration tests"""
  def setUp(self):
    mailer.app.config.from_object('config_test');
    self.app = mailer.app.test_client()


  def test_singleReceiver(self):
    postData = {
      'email_from'   : 'from_email@example.com',
      'email_to'     : 'to_email@example.com',
      'email_subject': 'Ny post i din eboks',
      'email_message': 'Ligegyldigt indhold'
    }

    rv = self.app.post('/send_mail', data=postData)
    parsedReturnData = json.loads(rv.data)
    self.assertEqual(parsedReturnData['status'], 'success')


  def test_multipleReceivers(self):
    postData = {
      'email_from': 'a@b.com', 
      'email_to': 'a@b.com,c@d.com,e@f.com', 
      'email_subject': 'Sub', 
      'email_message': 'Msg'
    }

    rv = self.app.post('/send_mail', data=postData)
    parsedReturnData = json.loads(rv.data)
    self.assertEqual(parsedReturnData['status'], 'success')


if __name__ == '__main__':
  unittest.main()