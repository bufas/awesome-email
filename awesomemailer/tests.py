import awesome_mailer
import unittest

class AwesomeMailerTestCase(unittest.TestCase):

  def setUp(self):
    awesome_mailer.app.config['TESTING'] = True
    self.app = awesome_mailer.app.test_client()

  def tearDown(self):
    pass

  def test_mandrillApiKey(self):
    rv = self.app.post('/send_mail', data=dict())
    assert 'PONG!' in rv.data

if __name__ == '__main__':
  unittest.main()