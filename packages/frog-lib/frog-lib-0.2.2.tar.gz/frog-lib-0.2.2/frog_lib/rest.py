import requests
import json
import logging
logger = logging.getLogger('rest')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

default_url = 'http://localhost:1337'

class Client():

  url = None
  token = None
  auth = False

  def __init__(self, url=None, token=None):

    if not url:
      url = 'http://localhost:1337'

    if token:
      self.token = token
      self.auth = True
    else:
      self.auth = False

    self.url = url


  def post(self, url='/', data={}):
    querystring = self.token

    payload = json.dumps(data).encode('utf-8')
    headers = {'content-type': 'application/json'}

    response = requests.request(
      "POST",
      self.url+url,
      data=payload,
      headers=headers,
      params=querystring
    )
    logger.info(response.text)
    return response.text

  def get(self, url='/', data={}):
    querystring = self.token

    payload = json.dumps(data).encode('utf-8')
    headers = {'content-type': 'application/json'}

    response = requests.request(
      "GET",
      self.url+url,
      # data=payload,
      headers=headers,
      params=querystring
    )
    logger.info(response.text)
    return response.text
