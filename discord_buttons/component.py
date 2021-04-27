from enum import Enum

from discord_buttons.type_hints import JSON


class ComponentType(Enum):
    Group = 1
    Button = 2


class Component:
    type: ComponentType

    def __init__(self, type: ComponentType):
        self.type = type

    def __repr__(self) -> str:
        return 'discord.interactions.components.Component(type={})'.format(self.type.value)

    def to_json(self) -> JSON:
        data = {
            'type': self.type.value
        }
        return data
