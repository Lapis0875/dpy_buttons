"""
discord_buttons
---------------
Wrapper supporting discord buttons feature.

@author Lapis0875 (lapis0875@kakao.com)
@copyright 2021
"""

import logging
from sys import stdout

from .channel import update
from .context import ButtonContext
from .button import ButtonStyle, Button
from .client import *

update()    # Replace features in discord.py to support buttons feature.

btn_logger = logging.getLogger('discord_buttons')
btn_logger.setLevel(logging.DEBUG)  # On development, DEBUG. On release, INFO
console_handler = logging.StreamHandler(stdout)
console_handler.setFormatter(
    logging.Formatter(
        style='{',
        fmt='[{asctime}] [{levelname}] {name}: {message}'
    )
)
btn_logger.addHandler(console_handler)
