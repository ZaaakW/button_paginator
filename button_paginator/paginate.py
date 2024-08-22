import discord
import logging

from asyncio import TimeoutError as AsyncTimeoutError
from contextlib import suppress
from typing import List, Union, Optional
from typing_extensions import override

from discord import ButtonStyle, Embed, HTTPException, Interaction, Message
from discord.ext.commands import Context
from discord.ui import Button, View

from .types import Page, Emoji, ButtonConfig

log = logging.getLogger(__name__)

class PaginatorButton(Button):
    """Button class for Paginator."""

    def __init__(
        self,
        emoji: str,
        style: ButtonStyle,
        action: str,
        paginator: Optional["Paginator"] = None
    ) -> None:
        super().__init__(emoji=emoji, style=style, custom_id=emoji)
        self.action: str = action
        self.paginator: Optional["Paginator"] = paginator

    async def callback(self, interaction: Interaction) -> None:
        """Callback function to handle button interactions."""
        await interaction.response.defer()

        if not self.paginator:
            return

        action_map = {
            "previous": self.previous_page,
            "next": self.next_page,
            "navigate": self.navigate,
            "cancel": self.cancel,
        }

        action = action_map.get(self.action)

        if action:
            await action(interaction)

    async def previous_page(self, _: Interaction) -> None:
        """Go to the previous page."""
        self.paginator.current_page = (
            self.paginator.current_page - 1
        ) % len(self.paginator.pages)
        await self.update_page()

    async def next_page(self, _: Interaction) -> None:
        """Go to the next page."""
        self.paginator.current_page = (
            self.paginator.current_page + 1
        ) % len(self.paginator.pages)
        await self.update_page()

    async def navigate(self, interaction: Interaction) -> None:
        """Navigate to a specific page."""
        for child in self.paginator.children:
            child.disabled = True

        await self.paginator.message.edit(view=self.paginator)

        embed = Embed(
            description="🔢 What **page** would you like to skip to?",
            color=0x6DB19A
        )

        prompt = await interaction.followup.send(
            embed=embed,
            ephemeral=True
        )
        try:
            response = await self.paginator.ctx.bot.wait_for(
                "message",
                timeout=15,
                check=lambda m: (
                    m.author.id == interaction.user.id and
                    m.channel.id == interaction.channel.id and
                    m.content.isdigit()
                )
            )
        except AsyncTimeoutError:
            for child in self.paginator.children:
                child.disabled = False

            await self.paginator.message.edit(view=self.paginator)
            await prompt.delete()
            return

        page_number = int(response.content) - 1
        if 0 <= page_number < len(self.paginator.pages):
            self.paginator.current_page = page_number

        for child in self.paginator.children:
            child.disabled = False

        with suppress(HTTPException):
            await prompt.delete()
            await response.delete()

        await self.update_page()

    async def cancel(self, _: Interaction) -> None:
        """Cancel the pagination."""
        with suppress(HTTPException):
            await self.paginator.message.delete()

    async def update_page(self) -> None:
        """Update the current page."""
        page = self.paginator.pages[self.paginator.current_page]

        if self.paginator.type == "embed":
            await self.paginator.message.edit(embed=page, view=self.paginator)
        else:
            await self.paginator.message.edit(content=page, view=self.paginator)


class Paginator(View):
    """Paginator view for handling multiple pages with buttons."""

    def __init__(
        self,
        ctx: Context,
        embeds: List[Embed | str],
        buttons: Optional[List[ButtonConfig]] = None
    ) -> None:
        super().__init__(timeout=180)

        self.ctx = ctx
        self.embeds = embeds
        self.current_page = 0
        self.message: Optional[Message] = None

        default_buttons = [
            {"emoji": Emoji._previous, "style": ButtonStyle.blurple, "action": "previous"},
            {"emoji": Emoji._next, "style": ButtonStyle.blurple, "action": "next"},
            {"emoji": Emoji._navigate, "style": ButtonStyle.grey, "action": "navigate"},
            {"emoji": Emoji._cancel, "style": ButtonStyle.red, "action": "cancel"},
        ]

        self.buttons = buttons or default_buttons
        self.add_buttons()

    def add_buttons(self) -> None:
        """Add buttons to the paginator."""
        for button_config in self.buttons:
            self.add_item(PaginatorButton(
                emoji=button_config["emoji"],
                style=button_config["style"],
                action=button_config["action"],
                paginator=self
            ))

    @property
    def type(self) -> str:
        """Return the type of content (embed or text)."""
        return "embed" if isinstance(self.pages[0], Embed) else "text"

    async def send(self, content: Union[str, Embed], **kwargs) -> Message:
        """Send the paginator message."""
        if self.type == "embed":
            return await self.ctx.send(embed=content, **kwargs)

        return await self.ctx.send(content=content, **kwargs)

    @override
    async def interaction_check(self, interaction: Interaction) -> bool:
        """Check if the interaction is from the original author."""
        if interaction.user.id != self.ctx.author.id:
            await interaction.channel.send(
                "You're not the **author** of this embed!",
                delete_after=5
            )
            return False

        return True

    async def on_timeout(self) -> None:
        """Disable buttons on timeout."""
        try:
            for child in self.children:
                child.disabled = True

            if self.message:
                await self.message.edit(view=self)
        except discord.errors.NotFound:
            log.info("Message was already deleted.")

    async def start(self) -> Message:
        """Start the paginator."""
        if len(self.embeds) == 1:
            self.message = await self.send(self.embeds[0])
        else:
            self.message = await self.send(self.embeds[self.current_page], view=self)

        return self.message