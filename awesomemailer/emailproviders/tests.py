import unittest
import os

import mailgun
import mandrillprovider as mandrill


MANDRILL_API_KEY = os.environ['MANDRILL_API_KEY_TEST']
MAILGUN_API_KEY = os.environ['MAILGUN_API_KEY']


class MandrillProviderTestCase(unittest.TestCase):
  def setUp(self):
    self.emailData = dict({
      'from'    : 'from_email@example.com',
      'to'      : ['to_email@example.com'],
      'subject' : 'Ny post i din eboks',
      'message' : 'Ligegyldigt indhold'
    })


  def tearDown(self):
    pass


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


class MailgunProviderTestCase(unittest.TestCase):
  def setUp(self):
    self.emailData = dict({
      'from'    : 'from_email@example.com',
      'to'      : ['to_email@example.com'],
      'subject' : 'Ny post i din eboks',
      'message' : 'Ligegyldigt indhold'
    })


  def tearDown(self):
    pass


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


if __name__ == '__main__':
  unittest.main()