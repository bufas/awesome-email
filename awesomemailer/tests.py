import mailer
import unittest
import json

class AwesomeMailerTestCase(unittest.TestCase):

  def setUp(self):
    mailer.app.config.from_object('config_test');
    self.app = mailer.app.test_client()

  def tearDown(self):
    pass

  def test_mandrillSendMail(self):
    postData = dict({
      'EMAIL_FROM'    : 'from_email@example.com',
      'EMAIL_TO'      : 'to_email@example.com',
      'EMAIL_SUBJECT' : 'Ny post i din eboks',
      'EMAIL_MESSAGE' : 'Ligegyldigt indhold'
    })

    rv = self.app.post('/send_mail', data=postData)
    realData = json.loads(rv.data)
    assert 'status' in realData and realData['status'] == 'sent'

if __name__ == '__main__':
  unittest.main()