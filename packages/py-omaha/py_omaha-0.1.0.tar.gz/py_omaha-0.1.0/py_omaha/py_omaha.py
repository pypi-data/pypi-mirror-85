import requests

class Omaha:
    token = None
    def __init__(self, url, username, password):
        self.base_url = url
        self.username = username
        self.password = password
        self.session = requests.Session()


    def login(self) -> bool:
        self.token = None
        url = self.base_url + 'api/v2/login'
        r = self.session.post(url, json={'username': self.username, 'password': self.password}, verify=False)
        result = r.json()
        if result["errorCode"] != 0:
            return False
        self.token = result["result"]["token"]
        return True

    def is_logged_in(self) -> bool:
        return self.token is not None

    def get_devices(self) -> dict:
        url = self.base_url + 'api/v2/sites/Default/devices?token=' + self.token + '&_=1604760408974'
        r = self.session.get(url, verify=False)
        return r.json()

    def patch_device(self, device, data) -> dict:
        url = self.base_url + 'api/v2/sites/Default/eaps/' + device + '?token=' + self.token
        r = self.session.patch(url, json=data, verify=False)
        return r.json()