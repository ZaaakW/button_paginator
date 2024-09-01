"""
discord pagination
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A python library create discord paginator to make you easy.

:copyright: (c) 2024 @zaaakw
:license: MIT

"""

from .paginate import Paginator, PaginatorButton
from .types import Emoji, Page, ButtonConfig

__all__ = [
    "Paginator",
    "PaginatorButton",
    "ButtonConfig",
    "Emoji",
    "Page"
]
