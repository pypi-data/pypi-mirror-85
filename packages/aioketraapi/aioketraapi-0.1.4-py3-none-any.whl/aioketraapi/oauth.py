import aiohttp
import json

class OAuthTokenResponse:
    def __init__(self, access_token=None, refresh_token=None, expires_at=None, **_):
        if access_token is None:
            raise ValueError("oauth_token must not be None")
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_at = expires_at

    def write_to_file(self, fn):
        with open(fn, 'w') as f:
            obj_to_write = {**self.__dict__}
            for key in list(obj_to_write.keys()):
                if obj_to_write[key] is None:
                    obj_to_write.pop(key)
            f.write(json.dumps(obj_to_write))

    @classmethod
    def load_from_file(cls, fn):
        with open(fn) as f:
            json_obj = json.load(f)
            return cls(**json_obj)


    @classmethod
    async def request_token(cls, client_id, client_secret, username, password, loop=None):
        url = 'https://my.goketra.com/oauth/token'
        request_data = {"username": username, "password": password,
                        "grant_type": "password", "client_id": client_id,
                        "client_secret": client_secret}
        async with aiohttp.ClientSession(loop=loop) as session:
            async with session.post(url, json=request_data) as response:
                if response.status == 200:
                    content = await response.json()
                    return OAuthTokenResponse(**content)

