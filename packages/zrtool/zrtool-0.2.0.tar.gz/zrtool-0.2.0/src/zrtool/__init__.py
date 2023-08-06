# Copyright 2019-2020 Rémy Taymans <remytms@tsmail.eu>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

"""Package with tools to manage a ZoomR16 project."""

from os import environ

__productname__ = "zrtool"
__version__ = "0.2.0"
__license__ = "GPL-3.0-or-later"

__all__ = ["cli"]

PGRNAME = __productname__
FLACBIN = environ.get(PGRNAME.upper() + "_FLAC_BIN", "flac")
