import mandrill

def send(data):
  try:
    mandrill_client = mandrill.Mandrill('VJvnDXTPNEiZsuH0mO0c4A')

    message = dict({
      # 'attachments': [{
      #   'content': 'ZXhhbXBsZSBmaWxl',
      #   'name': 'myfile.txt',
      #   'type': 'text/plain'}],
      # 'auto_html': None,
      # 'auto_text': None,
      # 'bcc_address': 'message.bcc_address@example.com',
      'from_email': data['from'],
      # 'from_name': 'Example Name',
      # 'global_merge_vars': [{
      #   'content': 'merge1 content', 
      #   'name': 'merge1'}],
      # 'google_analytics_campaign': 'message.from_email@example.com',
      # 'google_analytics_domains': [
      #   'example.com'],
      # 'headers': {
      #   'Reply-To': 'message.reply@example.com'},
      # 'html': '<p>Example HTML content</p>',
      # 'images': [{
      #   'content': 'ZXhhbXBsZSBmaWxl',
      #   'name': 'IMAGECID',
      #   'type': 'image/png'}],
      # 'important': False,
      # 'inline_css': None,
      # 'merge': True,
      # 'merge_language': 'mailchimp',
      # 'merge_vars': [{
      #   'rcpt': 'recipient.email@example.com',
      #   'vars': [{
      #     'content': 'merge2 content', 
      #     'name': 'merge2'}]}],
      # 'metadata': {
      #   'website': 'www.example.com'},
      # 'preserve_recipients': None,
      # 'recipient_metadata': [{
      #   'rcpt': 'recipient.email@example.com',
      #   'values': {
      #     'user_id': 123456}}],
      # 'return_path_domain': None,
      # 'signing_domain': None,
      # 'subaccount': 'customer-123',
      'subject': data['subject'],
      # 'tags': [
      #   'password-resets'],
      'text': data['message'],
      'to': [],
      # 'track_clicks': None,
      # 'track_opens': None,
      # 'tracking_domain': None,
      # 'url_strip_qs': None,
      # 'view_content_link': None
    })

    message['to'] = [{'email':mail, 'type':'to'} for mail in data['to']]

    result = mandrill_client.messages.send(message=message)
    return result[0]
  except mandrill.Error, e:
    # print 'waddafuq'
    # print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
    raise
