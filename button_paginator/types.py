from typing import Union, Dict
from discord import Embed, ButtonStyle

Page = Union[Embed, str]
ButtonConfig = Dict[str, Union[str, ButtonStyle]]

class Emoji:
    _previous: str = "⬅️"
    _next: str = "➡️"
    _navigate: str = "🔢"
    _cancel: str = "❌"