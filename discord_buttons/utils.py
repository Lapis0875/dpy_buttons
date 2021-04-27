from mailbox import Message
from typing import Dict

from discord import Member, User

from discord_buttons.type_hints import JSON


class SingletonMeta(type):
    __instances__: Dict = {}

    def __call__(cls, *args, **kwargs) -> type:
        if cls not in cls.__instances__:
            cls.__instances__[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls.__instances__[cls]


def get_data_from_user(user: User) -> JSON:
    data: JSON = {
        'username': user.name,
        'id': user.id,
        'discriminator': user.discriminator,
        'public_flags': user.public_flags.value,
        'bot': user.bot,
        'avatar': user.avatar
    }
    return data


def get_data_from_member(member: Member) -> JSON:
    data: JSON = {
        'user': get_data_from_user(member._user),
        'roles': [
            role.id
            for role in member.roles
        ],
        'premium_since': member.premium_since,
        'permissions': member.guild_permissions,
        'pending': member.pending,
        'nick': member.nick,
        'joined_at': member.joined_at
        # mute, is_pending, deaf : missing in Member.

    }
    return data


def get_data_from_msg(msg: Message) -> JSON:
    data: JSON = {
        'type': msg.type,
        'id': msg.id,
        'channel_id': msg.channel.id,
        'author': get_data_from_user(msg.author),
        'attachments': msg.attachments,
        'timestamp': msg.created_at,
        'pinned': msg.pinned,
        'tts': msg.tts,
        'edited_timestamp': msg.edited_at,
        'flags': msg.flags,
        'mentions': [role.id for role in msg.mentions],
        'mention_roles': [role.id for role in msg.role_mentions],
        'mention_everyone': msg.mention_everyone,
        'content': msg.content,
        'embeds': msg.embeds
    }
    return data