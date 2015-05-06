import unittest
import os

from emailhelper import EmailDataHandler

import mailgun
import mandrillprovider as mandrill


MANDRILL_API_KEY = os.environ['MANDRILL_API_KEY_TEST']
MAILGUN_API_KEY = os.environ['MAILGUN_API_KEY_TEST']


class MandrillProviderTestCase(unittest.TestCase):
  def setUp(self):
    self.defaultDataHandler = EmailDataHandler('a@b.com', 'c@d.com', 'Sub', 'Msg')


  def tearDown(self):
    pass


  def test_mandrillWrongKey(self):
    res = mandrill.send(self.defaultDataHandler, 'WRONG API KEY')
    self.assertEqual(len(res['successes']), 0)
    self.assertEqual(len(res['errors']), 1)
    self.assertTrue('mail' in res['errors'][0])
    self.assertTrue('reason' in res['errors'][0])


  def test_mandrillSender(self):
    res = mandrill.send(self.defaultDataHandler, MANDRILL_API_KEY)
    self.assertEqual(len(res['successes']), 1)
    self.assertEqual(len(res['errors']), 0)
    self.assertEqual(res['successes'][0], 'c@d.com')


class MailgunProviderTestCase(unittest.TestCase):
  def setUp(self):
    self.defaultDataHandler = EmailDataHandler('a@b.com', 'c@d.com', 'Sub', 'Msg')


  def tearDown(self):
    pass


  def test_mailgunWrongKey(self):
    res = mailgun.send(self.defaultDataHandler, 'WRONG API KEY')
    self.assertEqual(len(res['successes']), 0)
    self.assertEqual(len(res['errors']), 1)
    self.assertTrue('mail' in res['errors'][0])
    self.assertTrue('reason' in res['errors'][0])


  def test_mailgunSender(self):
    res = mailgun.send(self.defaultDataHandler, MAILGUN_API_KEY)
    self.assertEqual(len(res['successes']), 1)
    self.assertEqual(len(res['errors']), 0)
    self.assertEqual(res['successes'][0], 'c@d.com')


if __name__ == '__main__':
  unittest.main()