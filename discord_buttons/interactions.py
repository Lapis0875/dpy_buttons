from __future__ import annotations

import asyncio
from enum import Enum
from typing import Optional, Callable, Any, List

from discord import Member, User, Guild, Client, Embed, AllowedMentions
from discord.abc import Messageable
from discord.http import Route

from discord_buttons.button import ComponentType, Button, ButtonCache
from discord_buttons.type_hints import JSON, Function, CoroutineFunction


class InteractionType:
    Ping = 1
    ApplicationCommand = 2


class InteractionData:
    """Parent calss for all interaction datas"""

    @classmethod
    def is_valid(cls, data: JSON) -> bool:
        """
        Return if the data contains valid object of InteractionData's subclasses.
        This method must be implemented in subclasses.
        Args:
            data (Dict[str, Any]) : data object in interaction.
        Returns:
             boolean value if the data is valid or not.
        """
        pass

    @classmethod
    def parse(cls) -> InteractionData:
        """
        Parse interaction data object into python object.
        This method must be implemented in subclasses.
        Args:
            data (Dict[str, Any]) : data object in interaction.
        Returns:
            interaction data object wrapped in python.
        """
        pass


class ApplicationCommandInteractionData(InteractionData):
    @classmethod
    def is_valid(cls, data: JSON) -> bool:
        """
        Return if the data contains valid ApplicationCommandInteractionData object.
        Args:
            data (Dict[str, Any]) : data object in interaction.
        Returns:
             boolean value if the data is valid or not.
        """
        return 'id' in data and 'name' in data and 'resolved' in data and 'options' in data

    @classmethod
    def parse(cls, data) -> ApplicationCommandInteractionData:
        """
        Parse ApplicationCommandInteractionData object into python object.
        Args:
            data (Dict[str, Any]) : data object in interaction.
        Returns:
            ApplicationCommandInteractionData object wrapped in python.
        """
        return cls(
            id=data['id'],
            name=data['name'],
            resolved=data['resolved'],
            # Needs to be parsed into python object implementation : ApplicationCommandInteractionDataResolved
            options=data['options']
            # Needs to be parsed into python object implementation : List[ApplicationCommandInteractionDataOption]
        )

    def __init__(
            self,
            id: int,
            name: str,
            # ApplicationCommand features. Will be implemented later in 'discord_interactions' library.
            resolved: Optional[Any] = None,
            options: Optional[List[Any]] = None
    ):
        super(ApplicationCommandInteractionData, self).__init__()
        self.id: int = id
        self.name: str = name
        self.resolved = resolved
        self.options = options


class ButtonInteractionData(InteractionData):
    @classmethod
    def is_valid(cls, data) -> bool:
        """
        Return if the data contains valid ButtonInteractionData object.
        Args:
            data (Dict[str, Any]) : data object in interaction.
        Returns:
             boolean value if the data is valid or not.
        """
        return 'custom_id' in data and 'component_type' in data

    @classmethod
    def parse(cls, data) -> ButtonInteractionData:
        return cls(
            custom_id=data['custom_id'],
            component_type=data['component_type']
        )

    def __init__(
            self,
            custom_id: str,
            component_type: ComponentType
    ):
        super(ButtonInteractionData, self).__init__()
        self.custom_id: str = custom_id
        self.component_type: ComponentType = component_type
        self._button: Optional[Button] = ButtonCache().get_button(custom_id)


class InteractionContext:
    def __init__(self, client: Client):
        self.client = client

    def from_json(self, data): pass

    async def respond(
            self,
            response_type: InteractionResponseType,
            content: Optional[str] = None,
            embed: Optional[Embed] = None,
            embeds: Optional[List[Embed]] = None,
            allowed_mentions: Optional[AllowedMentions] = None,
            tts: Optional[bool] = None,
            flags: Optional[int] = None
    ):
        state = self.client._get_state()
        data: JSON = {}

        if content:
            data['content'] = content

        if embed and embeds:
            embeds.append(embed)
        elif embed:
            embeds = [embed]

        if embeds and len(embeds) <= 10:
            data['embeds'] = list(map(embed.to_dict() for embed in embeds))

        if allowed_mentions:
            if state.allowed_mentions:
                data['allowed_mentions'] = state.allowed_mentions.merge(allowed_mentions).to_dict()
            else:
                data['allowed_mentions'] = allowed_mentions.to_dict()
        else:
            data['allowed_mentions'] = state.allowed_mentions and state.allowed_mentions.to_dict()

        if tts:
            data['tts'] = tts

        await self.client.http.request(
            Route("POST", f"/interactions/{self.interaction_id}/{self.interaction_token}/callback"),
            json={"type": response_type.value, "data": data},
        )


class Interaction:
    """
    Interaction object. Waiting for discord.py's interaction features to be released :D
    """

    @classmethod
    async def from_data(cls, data: JSON, dpy_client: Client):
        if 'guild_id' in data:
            guild_id: int = data['guild_id']
            guild: Optional[Guild] = dpy_client.get_guild(guild_id) or (await dpy_client.fetch_guild(guild_id))
        else:
            guild = None

        if 'channel_id' in data:
            channel_id: int = data['channel_id']
            channel: Optional[Messageable] = dpy_client.get_channel(channel_id) or (
                await dpy_client.fetch_channel(channel_id))
        else:
            channel = None

        if 'user' in data:
            user: Optional[User] = dpy_client.get_user(data['user']['id'])
            member = None
        elif 'member' in data:
            member_id: int = data['member']['user']['id']
            if guild is None:
                raise ValueError('Interaction.guild is not found! Cancel parsing member object.')
            member: Optional[Member] = guild.get_member(member_id) or (await guild.fetch_member(member_id))
            user = member._user
        else:
            user = None
            member = None

        return cls(
            id=data['id'],
            application_id=data['application_id'],
            token=data['token'],
            version=data['version'],
            dpy_client=dpy_client,
            data=cls.parse_interaction_data(data['data']),
            guild_id=data['guild_id'],
            guild=guild,
            channel_id=data['channel_id'],
            channel=channel,
            member=member,
            user=user
        )

    @classmethod
    def parse_interaction_data(cls, data) -> Optional[InteractionData]:
        if ApplicationCommandInteractionData.is_valid(data):
            return ApplicationCommandInteractionData.parse(data)
        elif ButtonInteractionData.is_valid(data):
            return ButtonInteractionData.parse(data)
        else:
            return None

    def __init__(
            self,
            id: int,
            application_id: int,
            type: InteractionType,
            token: str,
            version: int,
            dpy_client: Client,
            data: Optional[JSON] = None,
            guild_id: Optional[int] = None,
            guild: Optional[Guild] = None,
            channel_id: Optional[int] = None,
            channel: Optional[Messageable] = None,
            member: Optional[Member] = None,
            user: Optional[User] = None
    ):
        self.id: int = id
        self.application_id: int = application_id
        self.type: InteractionType = type
        self.token: str = token
        self.version: int = version
        self.client: Client = dpy_client

        # discord objects
        self.guild_id: Optional[int] = guild_id
        self._guild: Optional[Guild] = guild
        self.channel_id: Optional[int] = channel_id
        self._channel: Optional[Messageable] = channel
        self.member: Optional[Member] = member
        self.user: Optional[User] = user

        # application command data
        self.data: Optional[JSON] = data  # Not used.

    @property
    def guild(self) -> Optional[Guild]:
        return self._guild

    @property
    def channel(self) -> Optional[Messageable]:
        return self._channel

    async def build_context(self) -> InteractionContext:
        pass


class InteractionResponseType(Enum):
    Pong = 1  # ACK a ping
    Acknowledge = 2  # @Deprecated ACK a command without sending a message, eating the user's input
    ChannelMessage = 3  # @Deprecated respond with a message, eating the user's input
    ChannelMessageWithSource = 4  # respond to an interaction with a message
    DeferredChannelMessageWithSource = 5  # ACK an interaction and edit a response later, the user sees a loading state

    @classmethod
    def from_value(cls, value: int) -> Optional[InteractionResponseType]:
        return next(
            filter(lambda m: m.value == value, cls.__members__.values()),
            None
        )
