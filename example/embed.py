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