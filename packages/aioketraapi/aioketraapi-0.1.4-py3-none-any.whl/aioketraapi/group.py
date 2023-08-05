from aioketraapi.models.group import Group as GroupModel
from aioketraapi.models.lamp_state import LampState as LampStateModel
from aioketraapi.api.group_operations_api import GroupOperationsApi



class Group(GroupModel):
    def __init__(self, group_model: GroupModel, hub):
        super().__init__(**group_model.to_dict())
        self.state = group_model.state
        self.hub = hub

    def update_state_from_model(self, lamp_state: LampStateModel):
        self.state = lamp_state

    async def update_state(self):
        async with self.hub.api_client() as api_client:
            updated_group = await GroupOperationsApi(api_client).groups_group_id_state_get(self.id)
            self.update_state_from_model(updated_group.content)

    async def set_state(self, lamp_state: LampStateModel, **kwargs):
        async with self.hub.api_client() as api_client:
            updated_group = await GroupOperationsApi(api_client).groups_group_id_state_put(self.id, lamp_state, **kwargs)
            self.update_state_from_model(updated_group.content)





