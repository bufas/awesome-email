import unittest
import json
import os

import mailer
from model import ProviderModel


class AwesomemailerTestCase(unittest.TestCase):
  def setUp(self):
    mailer.app.config.from_object('config_test');
    self.app = mailer.app.test_client()

    # Setup database
    mailer.db.create_all()
    p1 = ProviderModel('emailproviders.mandrillprovider', os.environ['MANDRILL_API_KEY_TEST'], 0, 0, 1)
    p2 = ProviderModel('emailproviders.mailgun', os.environ['MAILGUN_API_KEY_TEST'], 0, 0, 2)
    mailer.db.session.add(p1)
    mailer.db.session.add(p2)
    mailer.db.session.commit()


  def tearDown(self):
    # Clear database
    mailer.db.session.remove()
    mailer.db.drop_all()


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
