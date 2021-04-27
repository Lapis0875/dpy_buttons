from typing import Optional, List, Union
import discord
from discord.http import Route

from discord_buttons.interactions import InteractionContext
from discord_buttons.message import ComponentMessage
from discord_buttons.type_hints import JSON

__all__ = (
    'ButtonContext',
)


class ButtonContext(InteractionContext):
    def __init__(
            self,
            message: ComponentMessage,
            user: Union[discord.User, discord.Member],
            button: 'Button',
            interaction_id: str,
            raw_data: JSON
    ):
        super(ButtonContext, self).__init__()
        self.message: ComponentMessage = message
        self.channel: discord.abc.Messageable = message.channel
        self.user: Union[discord.User, discord.Member] = user
        if isinstance(self.user, discord.Member):
            self.guild: discord.Guild = message.guild
        else:
            self.guild = None

        self.button: 'Button' = button
        self.interaction_id: str = interaction_id
        self.raw_data: JSON = raw_data
        self.send = message.channel.send
        self.reply = message.reply

    async def respond(
            self,
            type: int,
            content: str,
            embed: Optional[discord.Embed] = None,
            embeds: Optional[List[discord.Embed]] = None,
            tts: Optional[bool] = None,
            flags: Optional[int] = None
    ):
        Route('POST', '')
