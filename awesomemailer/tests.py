import mailer
import unittest
import json

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

  def test_mailgunSender(self):
    import mailgunsender as mailer
    from config_test import MAILGUN_API_KEY

    res = mailer.send(self.emailData, MAILGUN_API_KEY)
    assert 'message' in res and res['message'].startswith('Queued.')

  def test_mandrillSender(self):
    import mandrillsender as mailer
    from config_test import MANDRILL_API_KEY as API_KEY

    res = mailer.send(self.emailData, API_KEY)
    assert 'status' in res and res['status'].startswith('sent')

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