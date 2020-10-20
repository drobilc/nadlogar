import requests
import json
from .encryption import AESCipher
from datetime import datetime
from enum import Enum

class FrancekUserRole(Enum):
    student = 0
    teacher = 1
    other = 2

class FrancekApiException(Exception):
    pass

class InvalidLogin(FrancekApiException):
    pass

class FrancekUser(object):

    def __init__(self, api, user_id, username):
        self.francek_api = api
        self.id = user_id
        self.username = username
    
    def get_role(self):
        return self.francek_api.get_user_role(self.id)
    
    def __str__(self):
        return '<FrancekUser id={}, username="{}">'.format(self.id, self.username)
    
    def __repr__(self):
        return '<FrancekUser id={}, username="{}">'.format(self.id, self.username)

class FrancekApi(object):

    BASE_URL = 'https://www.franček.si/apiext'

    def __init__(self, secret, source):
        self.source = source
        self.secret = secret

        self.LINK_ACCOUNT_URL = self.BASE_URL + '/linkaccount'
        self.GET_USER_LEVEL_URL = self.BASE_URL + '/getuserlevel'

        self.DEFAULT_HEADERS = {
            'ContentType': 'multipart/form-data'
        }

    def generate_api_key_dict(self, user_id, timestamp=None):
        if timestamp is None:
            timestamp = datetime.utcnow()
        
        return json.dumps({
            'source': self.source,
            'userid': user_id,
            'timestamp': timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')
        })
    
    def generate_api_key(self, user_id, timestamp=None):
        data = self.generate_api_key_dict(user_id, timestamp=timestamp)
        return AESCipher.encrypt(self.secret, data)

    def login(self, username, password):
        api_key = self.generate_api_key(user_id='')

        response = requests.post(
            self.LINK_ACCOUNT_URL,
            headers=self.DEFAULT_HEADERS,
            data={
                'apikey': api_key,
                'username': username,
                'password': password
            }
        )
        print(response.text)

        response_json = response.json()

        if 'error' in response_json:
            raise FrancekApiException(response_json['error'])

        if response_json['result'] == 0:
            raise FrancekInvalidLogin

        return FrancekUser(self, response_json['result'], username)
    
    def _parse_user_role(self, json_response):
        role_value = json_response['role']
        return FrancekUserRole(role_value)

    def get_user_role(self, user_id):
        api_key = self.generate_api_key(user_id=user_id)
        response = requests.post(
            self.GET_USER_LEVEL_URL,
            headers=self.DEFAULT_HEADERS,
            data={ 'apikey': api_key }
        )
        response_json = response.json()

        if 'error' in response_json:
            raise FrancekApiException(response_json['error'])

        return self._parse_user_role(response_json['result'])

class FrancekApiTest(FrancekApi):
    BASE_URL = 'https://francek.amebis.si/apiext'