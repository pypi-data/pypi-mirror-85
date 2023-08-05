import aiohttp
from aioketraapi.api.keypad_operations_api import KeypadOperationsApi
from aioketraapi.api.group_operations_api import GroupOperationsApi
from aioketraapi.api_client import ApiClient
from aioketraapi.configuration import Configuration
from aioketraapi.keypad import Keypad
from aioketraapi.group import Group





class N4Hub():
    def __init__(self, url_base, oauth_token, loop=None):
        self.url_base = url_base
        self.oauth_token = oauth_token
        self.is_local = "api.goketra.com" not in url_base
        self.client_config = Configuration()
        self.client_config.host = self.url_base
        self.client_config.username = "na"
        self.client_config.password = self.oauth_token
        self.client_config.loop = loop
        if self.is_local:
            self.client_config.verify_ssl = False


    @classmethod
    async def get_hub(cls, installation_id, oauth_token, use_cloud = False, loop=None):
        query_url = f"https://my.goketra.com/api/n4/v1/query?installation_id={installation_id}"
        async with aiohttp.ClientSession(loop=loop) as session:
            async with session.get(query_url) as response:
                if response.status == 200:
                    hub_query_resp = await response.json()
                    if hub_query_resp['success'] == 'true' and len(hub_query_resp['content']) > 0:
                        first_hub = hub_query_resp['content'][0]
                        if use_cloud:
                            url = f"https://api.goketra.com/{installation_id}/{first_hub['serial_number']}/webAPI/api/v1"
                            return N4Hub(url, oauth_token)
                        else:
                            url = f"https://{first_hub['internal_ip']}/ketra.cgi/api/v1"
                            return N4Hub(url, oauth_token, loop)
            return None

    def api_client(self):
        return ApiClient(configuration=self.client_config)

    async def get_keypads(self, **kwargs):
        async with self.api_client() as api_client:
            kp_api = KeypadOperationsApi(api_client)
            response_model = await kp_api.keypads_get(**kwargs)
            return [Keypad(keypad, self) for keypad in response_model.content]

    async def get_groups(self, include_internal=False, **kwargs):
        async with self.api_client() as api_client:
            kp_api = GroupOperationsApi(api_client)
            response_model = await kp_api.groups_get(**kwargs)
            return [Group(group, self) for group in response_model.content if include_internal or 'Internal_MasterGroup' not in group.name]



