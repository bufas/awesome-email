import mailer
import unittest
from mock import Mock
import json

import mailgunsender as mailgun
import mandrillsender as mandrill

import utils

from config_test import MANDRILL_API_KEY, MAILGUN_API_KEY

class AwesomeMailerTestCase(unittest.TestCase):

  def setUp(self):
    mailer.app.config.from_object('config_test');
    self.app = mailer.app.test_client()

    self.emailData = dict({
      'from'    : 'from_email@example.com',
      'to'      : ['to_email@example.com'],
      'subject' : 'Ny post i din eboks',
      'message' : 'Ligegyldigt indhold'
    })

    self.mail1 = 'email@example.com'
    self.mail2 = 'my.name@domain.eu'
    self.mail3 = 'wat7900@aroundtheworld.org'
    self.mail4 = 'sharklazers@guerillamail.com'
    self.invalidMail1 = 'noathere.com'
    self.invalidMail2 = 'asdf'

    self.providerMandrill = ('mandrillsender', MANDRILL_API_KEY)
    self.providerMailgun = ('mailgunsender', MAILGUN_API_KEY)

  def tearDown(self):
    pass

  # Test the utils file

  def test_sendEmailOneProvider(self):
    res = utils.sendEmails(self.emailData, [self.providerMandrill])
    self.assertEquals(len(res['successes']), 1)
    self.assertEquals(len(res['errors']), 0)

  def test_sendEmailMultipleProviders(self):
    res = utils.sendEmails(self.emailData, [self.providerMandrill, self.providerMailgun])
    self.assertEquals(len(res['successes']), 1)
    self.assertEquals(len(res['errors']), 0)

  # TODO test that the second provider is used if the first one errors completely
  # TODO test that the second provider sends the rest of the emails if the first one only sends part of the mails

  def test_sanitizeTooFewArgs(self):
    res = utils.sanitize({})
    self.assertTrue('from' in res)
    self.assertTrue('to' in res)
    self.assertTrue('subject' in res)
    self.assertTrue('message' in res)

  def test_sanitizeEmptyListForTo(self):
    res = utils.sanitize({})
    self.assertTrue(type(res['to']) is list)
    self.assertEqual(len(res['to']), 0)

  def test_validateValidSingleTo(self):
    data = {'from' : self.mail1, 'to' : [self.mail1], 'subject' : '', 'message' : ''}
    self.assertIsNone(utils.isValid(data))

  def test_validateValidMultipleTo(self):
    data = {'from' : self.mail1, 
            'to' : [self.mail1, self.mail2, self.mail3], 
            'subject' : '', 
            'message' : ''}
    self.assertIsNone(utils.isValid(data))

  def test_validateInvalidEmptyFrom(self):
    data = {'from' : '', 'to' : [self.mail1], 'subject' : '', 'message' : ''}
    res = utils.isValid(data)
    self.assertTrue('Required' in res['from'])

  def test_validateInvalidEmptyTo(self):
    data = {'from' : 'from_email@example.com', 'to' : [], 'subject' : '', 'message' : ''}
    res = utils.isValid(data)
    self.assertTrue('Required' in res['to'])

  def test_validateInvalidInvalidFrom(self):
    data = {'from' : self.invalidMail1, 'to' : [self.mail1], 'subject' : '', 'message' : ''}
    res = utils.isValid(data)
    self.assertTrue('Invalid email' in res['from'])

  def test_validateInvalidInvalidToAll(self):
    data = {'from' : self.mail1, 
            'to' : [self.invalidMail1, self.invalidMail2], 
            'subject' : '', 
            'message' : ''}
    res = utils.isValid(data)
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
    res = utils.isValid(data)
    self.assertEqual(len(res['to']), 1)
    self.assertEqual(res['to'][0]['email'], self.invalidMail1)
    self.assertEqual(res['to'][0]['reason'], 'Invalid email')

  # Test the mailgun adapter

  def test_mailgunWrongKey(self):
    res = mailgun.send(self.emailData, 'WRONG API KEY')
    self.assertEqual(len(res['successes']), 0)
    self.assertEqual(len(res['errors']), 1)
    self.assertTrue('mail' in res['errors'][0])
    self.assertTrue('reason' in res['errors'][0])

  def test_mailgunSender(self):
    res = mailgun.send(self.emailData, MAILGUN_API_KEY)
    self.assertEqual(len(res['successes']), 1)
    self.assertEqual(len(res['errors']), 0)
    self.assertEqual(res['successes'][0], self.emailData['to'][0])

  # Test the mandrill adapter

  def test_mandrillWrongKey(self):
    res = mandrill.send(self.emailData, 'WRONG API KEY')
    self.assertEqual(len(res['successes']), 0)
    self.assertEqual(len(res['errors']), 1)
    self.assertTrue('mail' in res['errors'][0])
    self.assertTrue('reason' in res['errors'][0])

  def test_mandrillSender(self):
    res = mandrill.send(self.emailData, MANDRILL_API_KEY)
    self.assertEqual(len(res['successes']), 1)
    self.assertEqual(len(res['errors']), 0)
    self.assertEqual(res['successes'][0], self.emailData['to'][0])

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