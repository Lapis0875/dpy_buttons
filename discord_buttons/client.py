import json
from typing import List, Optional
from logging import getLogger

import discord
from discord import Client, AutoShardedClient, Guild, Member, User
from discord.abc import Messageable
from discord.ext.commands.bot import BotBase
from discord.http import Route

from discord_buttons import Button, ButtonCache, ButtonContext
from discord_buttons.message import ComponentMessage
from discord_buttons.type_hints import JSON

__all__ = (
    'ButtonClient',
    'AutoShardedButtonClient',
    'ButtonBot',
    'AutoShardedButtonBot'
)

btn_logger = getLogger('discord_buttons')


class ButtonHandler:
    def __init__(self, *args, **kwargs):
        self.buttons: List[Button] = []

    async def on_socket_response(self, msg: JSON):
        """
        Event handler for socket response event in discord.py
        :param msg: gateway payload received in discord.py client's websocket.
        """

        if msg['t'] != 'INTERACTION_CREATE':
            # This event handler only handles 'INTERACTION_CREATE' event, so other events are dismissed.
            return

        btn_logger.debug("ButtonHandler : 'INTERACTION_CREATE' Event received in websocket. Debugging gateway payload :\n{}".format(
            json.dumps(msg, ensure_ascii=False, indent=2)
        ))
        data = msg['d']
        btn_logger.debug('ButtonHandler : Event data from gateway payload : {}'.format(
            json.dumps(data, ensure_ascii=False, indent=2)
        ))

        custom_id = data['data']['custom_id']
        btn: Optional[Button] = ButtonCache().get_button(custom_id)
        btn_logger.debug(f'btn : {btn}')
        if btn is not None:
            data = msg['d']
            state = self._get_state()

            channel_id: int = data['channel_id']
            btn_logger.debug(f'channel.id : {channel_id}')

            if 'guild_id' in data and 'member' in data:
                # Interaction from guild
                guild_id: int = data['guild_id']
                btn_logger.debug('Interaction from guild : id = {}'.format(guild_id))
                guild: Optional[Guild] = self.get_guild(guild_id)
                btn_logger.debug('- Guild : {}'.format(guild))
                if guild is not None:
                    member: Member = Member(data=data['member'], guild=guild, state=state)
                    btn_logger.debug('member : {}'.format(member))
                    channel: Optional[Messageable] = guild.get_channel(channel_id)
                    btn_logger.debug('guild.get_channel(channel.id) : {}'.format(channel))

                msg: ComponentMessage = ComponentMessage(state=state, channel=channel, data=data['message'])
                await btn.invoke(
                    ButtonContext(msg, member, btn, data['id'], raw_data=data)
                )

            elif 'user' in data:
                # Interaction from channel
                user: User = User(data=data['user'], state=state)
                btn_logger.debug('user : {}'.format(user))
                channel: Optional[Messageable] = self.get_channel(channel_id)
                btn_logger.debug('Client.get_channel(channel.id) : {}'.format(channel))

                msg: ComponentMessage = ComponentMessage(state=state, channel=channel, data=data['message'])
                await btn.invoke(
                    ButtonContext(msg, user, btn, data['id'], raw_data=data)
                )


class ButtonClient(Client, ButtonHandler):
    """
    Represents client which can handle discord buttons feature.

    This class is a subclass of :class:'discord.Client' and as a result,
    you can do anything that you can do with a :class:'discord.Client', you can do with
    this client.
    """
    pass


class AutoShardedButtonClient(AutoShardedClient, ButtonHandler):
    """
    This is similar to :class:`.ButtonClient` except that it is inherited from
    :class:`discord.AutoShardedClient` instead.
    """
    pass


class ButtonBot(BotBase, ButtonClient):
    """
    Represents a discord bot that supports discord button features.

    This class is a subclass of :class:`discord_buttons.ButtonClient` and as a result
    anything that you can do with a :class:`discord_buttons.ButtonClient` you can do with
    this bot.
    """
    pass


class AutoShardedButtonBot(BotBase, AutoShardedButtonClient):
    """
    This is similar to :class:`.ButtonBot` except that it is inherited from
    :class:`discord.AutoShardedClient` instead.
    """
    pass


