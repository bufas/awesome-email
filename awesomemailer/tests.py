import mailer
import unittest
import json

import mailgunsender as mailgun
import mandrillsender as mandrill

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

  def tearDown(self):
    pass

  def test_mailgunWrongKey(self):
    res = mailgun.send(self.emailData, 'WRONG API KEY')
    self.assertEqual(len(res['successes']), 0)
    self.assertEqual(len(res['errors']), 1)
    self.assertTrue('mail' in res['errors'][0])
    self.assertTrue('reason' in res['errors'][0])

  def test_mailgunSender(self):
    from config_test import MAILGUN_API_KEY

    res = mailgun.send(self.emailData, MAILGUN_API_KEY)
    self.assertEqual(len(res['successes']), 1)
    self.assertEqual(len(res['errors']), 0)
    self.assertEqual(res['successes'][0], self.emailData['to'][0])

  def test_mandrillWrongKey(self):
    res = mandrill.send(self.emailData, 'WRONG API KEY')
    self.assertEqual(len(res['successes']), 0)
    self.assertEqual(len(res['errors']), 1)
    self.assertTrue('mail' in res['errors'][0])
    self.assertTrue('reason' in res['errors'][0])

  def test_mandrillSender(self):
    from config_test import MANDRILL_API_KEY as API_KEY

    res = mandrill.send(self.emailData, API_KEY)
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