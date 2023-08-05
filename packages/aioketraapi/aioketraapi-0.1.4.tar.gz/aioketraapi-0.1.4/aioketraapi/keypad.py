from aioketraapi.models.keypad import Keypad as KeypadModel
from aioketraapi.models.button import Button as ButtonModel
from aioketraapi.models.level import Level as LevelModel
from aioketraapi.api.keypad_operations_api import KeypadOperationsApi



class Keypad(KeypadModel):
    def __init__(self, keypad_model: KeypadModel, hub):
        super().__init__(**keypad_model.to_dict())
        self.hub = hub
        self._buttons = [KeypadButton(button, self, hub) for button in keypad_model.buttons]
        self._button_map = {}
        for button in self._buttons:
            self._button_map[button.id] = button

    def update_from_model(self, keypad_model: KeypadModel):
        for k,v in keypad_model.to_dict().items():
            setattr(self, k, v)
        for button in keypad_model.buttons:
            self._button_map[button.id].update_from_model(button)

    @property
    def buttons(self):
        return self._buttons

    @buttons.setter
    def buttons(self, buttons):
        pass


class KeypadButton(ButtonModel):
    def __init__(self, button_model: ButtonModel, keypad: Keypad, hub):
        super().__init__(**button_model.to_dict())
        self.keypad = keypad
        self.hub = hub

    def update_from_model(self, button_model: ButtonModel):
        for k,v in button_model.to_dict().items():
            setattr(self, k, v)

    async def activate(self, level=65535):
        async with self.hub.api_client() as api_client:
            updated_keypad = await KeypadOperationsApi(api_client).keypads_keypad_id_buttons_button_id_activate_post(
                self.keypad.id,
                self.id,
                LevelModel(level))
            self.keypad.update_from_model(updated_keypad.content)

    async def deactivate(self):
        async with self.hub.api_client() as api_client:
            updated_keypad = await KeypadOperationsApi(api_client).keypads_keypad_id_buttons_button_id_deactivate_post(
                self.keypad.id,
                self.id,
                LevelModel())
            self.keypad.update_from_model(updated_keypad.content)

    @property
    def scene_name(self):
        _, _, kp_name = self.keypad.name.rpartition('/')
        return f"{kp_name} {self.name}"

