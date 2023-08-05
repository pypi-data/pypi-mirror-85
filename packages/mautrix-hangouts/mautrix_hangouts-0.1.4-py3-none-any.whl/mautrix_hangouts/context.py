# mautrix-hangouts - A Matrix-Hangouts puppeting bridge
# Copyright (C) 2019 Tulir Asokan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from typing import Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    import asyncio

    from mautrix.appservice import AppService

    from .__main__ import HangoutsBridge
    from .config import Config
    from .matrix import MatrixHandler
    from .web import HangoutsAuthServer


class Context:
    az: 'AppService'
    config: 'Config'
    loop: 'asyncio.AbstractEventLoop'
    bridge: 'HangoutsBridge'
    auth_server: 'HangoutsAuthServer'
    mx: Optional['MatrixHandler']

    def __init__(self, az: 'AppService', config: 'Config', loop: 'asyncio.AbstractEventLoop',
                 auth_server: 'HangoutsAuthServer', bridge: 'HangoutsBridge') -> None:
        self.az = az
        self.config = config
        self.loop = loop
        self.bridge = bridge
        self.mx = None
        self.auth_server = auth_server

    @property
    def core(self) -> Tuple['AppService', 'Config', 'asyncio.AbstractEventLoop']:
        return self.az, self.config, self.loop
