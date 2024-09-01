"""
MIT License

Copyright (c) 2024 @zaaakw

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
DEALINGS IN THE SOFTWARE.
"""

from button_paginator import Paginator, Emoji
from discord import Embed

import discord

intents = discord.Intents.default()
intents.message_content = True

bot = Pagination(command_prefix="!", intents=intents)

@bot.command()
async def paginate(self,ctx):
    embeds = [
        discord.Embed(
            title="Page 1", description="Description 1"
        ), 
        discord.Embed(
            title="Page 2", description="Description 2"
        ), 
        discord.Embed(
            title="Page 3", description="Description 3"
        )
    ]

    paginator = Paginator(
        ctx=ctx,
        embeds=embeds,
        buttons=[
            {"emoji": Emoji._previous, "style": discord.ButtonStyle.blurple, "action": "previous"},
            {"emoji": Emoji._next, "style": discord.ButtonStyle.blurple, "action": "next"},
            {"emoji": Emoji._navigate, "style": discord.ButtonStyle.grey, "action": "navigate"},
            {"emoji": Emoji._cancel, "style": discord.ButtonStyle.red, "action": "cancel"},
        ] # Can be left as none for default buttons, or you can customize them.
    )

    message = await paginator.start()

bot.run("YOUR_BOT_TOKEN")
