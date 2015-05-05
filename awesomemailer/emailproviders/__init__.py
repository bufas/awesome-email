"""
This package contains modules which are able to send emails
using different providers.

Each module provides a single function `send` that takes the 
email data as well as an API key. The data must be given as 
a reference to the EmailDataHandler class.

The return value of the function is a dict containing two keys
successes and errors. 

  successes: a list of addresses that the email was successfully 
             sent to. The email is not necessarily received yet, 
             but it is guaranteed that it will be sent by 
             the provider. 
  errors:    a list of dicts, one for each receiving email 
             address that failed. The dict contains two values, 
             mail, which maps to the failed address and reason, 
             which is a string representing the reason of 
             failure.
"""