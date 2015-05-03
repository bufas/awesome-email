import mailer
import unittest

class AwesomeMailerTestCase(unittest.TestCase):

  def setUp(self):
    mailer.app.config['TESTING'] = True
    self.app = mailer.app.test_client()

  def tearDown(self):
    pass

  def test_mandrillApiKey(self):
    rv = self.app.post('/send_mail', data=dict())
    assert 'PONG!' in rv.data

if __name__ == '__main__':
  unittest.main()