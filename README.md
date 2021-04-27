# dpy_buttons

wrapper library for discord.py, providing discord buttons feature.

## Future of the library
Will be merged into discord interaction api library, [discord_interactions](https://github.com/Lapis0875/discord_interactions.py)

1. Future structure :
```
discord_interactions
ㄴslash_commands
  ㄴ ...
ㄴcomponents
  ㄴbuttons // This project
    ㄴ ..
  ㄴ ..     // Prepare for future components
```

2. Future implementation
```py
# Before
class Button: ...

# After
class Component: ... # Parent class for all components
class Button(Component): ...
```


## Example
```python
from discord_buttons import Button, ButtonStyle, ButtonContext, ButtonMessage, ButtonClient, ButtonCache

# Create button
btn_red = Button(label='Red Button!', style=ButtonStyle.Red, custom_id='red_btn')
btn_url = Button(label='URL Button!', style=ButtonStyle.URL, url='https://...')

# Register button click handler
@btn_red.listen  # Thinking about name 'on_click'
async def handler(ctx: ButtonContext):
    # send message on channel
    # sent messages are wrapped as a objet 'ButtonMessage', which extends discord.py's Message and contains Button objects
    msg: ButtonMessage = await ctx.send(...)
    # send reply on button's message
    await ctx.reply(...)
    # Access to clicked button
    print(ctx.button)


# Client object which extends discord.py's Client to handle button event on socket response event.
# ButtonBot, AutoshardedButtonClient, AutoShardedButtonBot are also available.
client = ButtonClient()

@client.event
async def on_message(msg):
    if msg.content == '!buttons':
        await msg.channel.send(
            # Buttons can be wrapped in 2-dimensional array
            # Internally, this is implemented using component with type 1.
            buttons=[
                [Button('Blurple Button!, ButtonStyle.Blurple, 'blurple_btn'), Button('Gray Button!', ButtonStyle.Gray, 'gray_btn')]
                # You can get Button instance which is created in other code using ButtonCache().get_button(custom_id)  *URL Buttons are not cached, so they can't be retrieved.
                # ButtonCache implements Singleton pattern, so whenever you create instance, you can get same object.
                [ButtonCache().get_button('red_btn'), Button('Green Button!', ButtonStyle.Green, 'green_btn')]
                [btn_url]
            ]
        )
```
