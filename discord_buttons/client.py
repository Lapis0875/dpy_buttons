import json
from typing import List
from logging import getLogger

from discord import Client, AutoShardedClient
from discord.ext.commands.bot import BotBase
from discord.http import Route

from discord_buttons import Button
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
        full_id = msg['d']['data']['custom_id']
        embed = msg['d']['message']['embeds'][0]
        content = 'test'
        embed['description'] = content

        # route = Route(
        #     'PATCH',
        #     '/channels/{channel_id}/messages/{message_id}',
        #     channel_id=msg['d']['channel_id'],
        #     message_id=msg['d']['message']['id']
        # )
        #
        # await self.http.request(
        #     route,
        #     json={
        #         'embed': embed,
        #         'components': msg['d']['message']['components']
        #     }
        # )


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


