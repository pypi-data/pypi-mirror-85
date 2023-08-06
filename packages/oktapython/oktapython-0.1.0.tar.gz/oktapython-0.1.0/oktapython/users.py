import requests


class Users:
    def __init__(self, url, api_key):
        self.api_url = url + '/api/v1/users/'
        self.get_headers = {
            'Authorization': f'SSWS {api_key}'
        }
        self.post_headers = {
            'Authorization': f'SSWS {api_key}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def get_user(self, user_id):
        url = self.api_url + user_id
        response = requests.get(url=url, headers=self.get_headers)
        return response.content
