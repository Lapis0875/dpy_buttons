import asyncio
from contextlib import suppress
from enum import Enum
from typing import Optional
from logging import getLogger

import discord

from discord_buttons.context import ButtonContext
from discord_buttons.type_hints import JSON, CoroutineFunction

__all__ = (
    'ButtonStyle',
    'Button'
)

btn_logger = getLogger('discord_buttons')


class ComponentType(Enum):
    Group = 1
    Button = 2


class ButtonStyle(Enum):
    Blurple = 1
    Gray = 2
    Green = 3
    Red = 4
    URL = 5
    Link = URL

    @classmethod
    def parse(cls, value: int):
        btn_logger.debug('ButtonStyle(Enum) : Try parsing value {} into ButtonStyle enumeration object.'.format(value))
        filtered = filter(
            lambda x: x.value == value,
            cls.__members__.values()
        )
        with suppress(StopIteration):
            enum = next(filtered)
            btn_logger.debug('ButtonStyle(Enum) : Parsed enumerate object using filter + next() : {}.'.format(enum))
            if enum is None:
                raise ValueError('Invalid value is passed in ButtonStyle.parse(value) : {} is not a valid button style integer.'.format(value))
            return enum


class Button:
    label: str
    style: ButtonStyle
    custom_id: Optional[str]
    url: Optional[str]
    __slots__ = ('label', 'style', 'custom_id', 'url', '_callback')

    @classmethod
    def fromJson(
            cls,
            data: JSON
    ):
        label: str = data['label']
        style: int = data['style']
        custom_id: Optional[str] = data.get('custom_id')
        url: Optional[str] = data.get('url')
        return cls(label, ButtonStyle.parse(style), custom_id, url)

    def __init__(
            self,
            label: str,
            style: ButtonStyle,
            custom_id: Optional[str]=None,
            url: Optional[str]=None
    ):
        self.label = label if isinstance(label, str) else str(label)
        self.style = style  # Raw value must be parsed in Button.fromJson()
        self.custom_id = custom_id or None
        self.url = url or None
        if self.custom_id is not None and self.url is not None:
            raise ValueError('Button object can have either custom_id (color styles) or url (style==url).')
        self._callback: Optional[CoroutineFunction] = None

    def toJson(self) -> JSON:
        data = {
            'type': ComponentType.Button.value,
            'style': self.style.value,
            'label': self.label
        }
        if self.custom_id:
            data['custom_id'] = self.custom_id
        if self.url:
            data['url'] = self.url
        return data

    def __repr__(self) -> str:
        return 'Discord.Button(label={},style={},custom_id={},url={})'.format(self.label, self.style.name, self.custom_id, self.url)

    def listen(self, callback: CoroutineFunction):
        if not asyncio.iscoroutinefunction(callback):
            raise TypeError('Callback function for Button object must be a coroutine function!')

        self._callback = callback

    async def invoke(
            self,
            message: discord.Message,
            user: discord.User,
            button: 'Button',
            interaction_id: str,
            raw_data: JSON
    ):
        if self._callback is not None:
            ctx = ButtonContext(
                message,
                user,
                button,
                interaction_id,
                raw_data
            )
            return await self._callback(ctx)
