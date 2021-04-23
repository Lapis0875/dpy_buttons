import json
from typing import List, Optional
from logging import getLogger

import discord
from discord import Client, AutoShardedClient
from discord.ext.commands.bot import BotBase
from discord.http import Route

from discord_buttons import Button, getButtonFromCache, ButtonContext
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
        btn_logger.debug('ButtonHandler : Event data from gateway payload : {}'.format(
            json.dumps(msg['d'], ensure_ascii=False, indent=2)
        ))

        custom_id = msg['d']['data']['custom_id']
        btn: Optional[Button] = getButtonFromCache(custom_id)
        print(btn)
        if btn is not None:
            guild_id: int = msg['d']['guild_id']
            try:
                # Not DMChannel
                guild: discord.Guild = self.get_guild(guild_id) or (await self.fetch_guild(guild_id))
            except:
                # DMChannel
                guild = None
            print(guild)

            channel_id: int = msg['d']['channel_id']
            channel: discord.abc.Messageable = guild.get_channel(channel_id) if guild is not None else (await self.fetch_channel(channel_id))
            print(channel)

            user_id: int = msg['d']['member']['user']['id']
            if guild is not None:
                user: discord.Member = guild.get_member(user_id) or (await guild.fetch_member(user_id))
            else:
                user: discord.User = self.get_user(user_id) or (await self.fetch_user(user_id))
            print(user)

            msg_id: int = msg['d']['message']['id']
            msg: discord.Message = await channel.fetch_message(msg_id)
            await btn.invoke(
                ButtonContext(msg, user, btn, msg['d']['id'], raw_data=msg['d'])
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


