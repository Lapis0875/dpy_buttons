from __future__ import annotations
from typing import List, Any, Union, Optional

from discord import Message, User, Member

from discord_buttons.button import ComponentType, Button
from discord_buttons.type_hints import JSON
from discord_buttons.utils import get_data_from_msg

__all__ = (
    'ComponentMessage',
    'parse_component',
    'parse_buttons'
)


def parse_component(components: List[JSON]) -> List[Any]:
    objects: List[Any] = []
    for component in components:
        if component['type'] == ComponentType.Group:
            objects.extend(parse_component(component['components']))
        elif component['type'] == ComponentType.Button:
            objects.append(Button.from_json(component))

    return objects


def parse_buttons(components: List[JSON]) -> Union[List[List[Button]], List[Button]]:
    buttons: List[Union[List[Button],Button]] = []
    for component in components:
        if component['type'] == ComponentType.Group:
            buttons.append(parse_buttons(component['components']))
        elif component['type'] == ComponentType.Button:
            buttons.append(Button.from_json(component))

    return buttons


class ComponentMessage(Message):
    @classmethod
    def fromMessage(cls, msg: Message, data: Optional[JSON] = None) -> ComponentMessage:
        return cls(
            state=msg._state,
            channel=msg.channel,
            data=data or get_data_from_msg(msg)
        )

    def __init__(self, *, state, channel, data: JSON):
        super(ComponentMessage, self).__init__(state=state, channel=channel, data=data)
        components: Optional[List[JSON]] = data.get('components')
        if components:
            self._buttons: List[List[Button]] = parse_buttons(components)
        else:
            self._buttons = []

    @property
    def buttons(self) -> List[List[Button]]:
        return self._buttons

    def get_button(self, custom_id: str) -> Optional[Button]:
        return next(filter(
            lambda btn: btn.custom_id == custom_id,
            self._buttons
        ), None)    # Return None if no elements are found.




