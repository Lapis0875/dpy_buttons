from typing import Optional, List
import discord
from discord_buttons.type_hints import JSON

__all__ = (
    'ButtonContext',
)


class ButtonContext:
    def __init__(
            self,
            message: discord.Message,
            user: discord.User,
            button: 'Button',
            interaction_id: str,
            raw_data: JSON
    ):
        self.message: discord.Message = message
        self.channel: discord.abc.Messageable = message.channel
        self.user: discord.User = user
        self.button: 'Button' = button
        self.interaction_id: str = interaction_id
        self.raw_data: JSON = raw_data
        self.send = message.channel.send
        self.reply = message.reply
