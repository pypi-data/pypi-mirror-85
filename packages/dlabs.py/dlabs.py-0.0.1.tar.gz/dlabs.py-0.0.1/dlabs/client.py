# -*- coding: utf-8 -*-

"""
MIT License

Copyright (c) 2020 Paul Przybyszewski

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from asyncio import sleep
from aiohttp import ClientSession
from discord.ext import commands
from typing import Union
from .exceptions import DLabsError, NoBotError


class Bot:
    """
    Class used to wrap a raw response into an :class:`object`

    Parameters
    ----------
    data: :class:`dict`
        The raw data to convert from
    """

    def __init__(self, data):
        self.name: Union[str, None] = data.get("name", None)
        self.avatar_url: Union[str, None] = data.get("avatar", None)
        self.owner_id: Union[int, None] = int(data.get("owner", None))
        self.short_description: Union[str, None] = data.get("sdescription", None)
        self.long_description: Union[str, None] = data.get("ldescription", None)
        self.render: Union[str, None] = data.get("render", None)
        self.uptime: Union[str, None] = data.get("uptime", None)

    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return self.owner_id


class Client:
    """
    The main class used to interact with the DLabs API.

    Parameters
    ----------
    bot: :class:`Union[discord.ext.commands.Bot, discord.ext.commands.AutoShardedBot]`
        The instance of a discord.py Bot to use

        .. note::
            If this is left unfilled, the only method available is :meth:`get_bot`
    token: :class:`str`
        The DLabs token to use to authenticate with the API
    autopost: :class:`bool`
        A :class:`bool` specifying whether or not to automatically post stats to the API (defaults to False)

        .. note::

            This is unavailable if the :param:`bot` wasn't passed
    post_shard_count: :class:`bool`
        A :class:`bool` specifying if the client should post the shard count to the API (defaults to True)
    verbose: :class:`bool`
        A :class:`bool` specifying if actions taken by the client should be printed (defaults to False)
    """

    def __init__(self, bot: Union[commands.Bot, commands.AutoShardedBot, None] = None, token: Union[str, None] = None,
                 autopost: bool = False, verbose: bool = False, post_shard_count: bool = True):

        self.bot: Union[commands.Bot, commands.AutoShardedBot, None] = bot

        self._autopost: bool = autopost
        self._post_shard_count: bool = post_shard_count
        self._verbose: bool = verbose

        # Can't post without a bot object
        if self.bot is None and autopost is True:
            raise DLabsError(
                "Cannot autopost stats without a `commands.Bot` object. Pass it in the function arguments.")

        self._ses: ClientSession = ClientSession()
        self._token: Union[str, None] = token

        if self._autopost:
            self._autopost_task = self.bot.loop.create_task(self._autopost_stats())

    async def get_bot(self, bot_id: Union[int, str]) -> Bot:
        """
        Get a bot from the DLabs API

        Parameters
        ----------
        bot_id: :class:`Union[:class:`int`, :class:`str`]`
            The Bot ID to get

        Returns
        -------
        Bot: :class:`Bot`
            The bot that was requested

        Raises
        ------
        AssertionError
            The HTTP session used by the client was terminated
        DLabsError
            Something went wrong while trying to get the bot
        """
        assert self._ses.closed is False, "Client session closed"
        res_ = await self._ses.get(f"https://bots.discordlabs.org/v2/bot/{str(bot_id)}")
        res = await res_.json()
        if str(res["error"]).lower() == "true":
            raise DLabsError(str(res["message"]))
        return Bot(dict(res))

    async def post_stats(self):
        """
        Manually called to post stats to the DLabs API.
        For this to work,
        you have to pass a discord.py bot instance into the initialization of the DLabs client.
        To post automatically instead, just pass in verbose=True into the client initialization and don't use this

        Raises
        ------
        AssertionError
            The HTTP session used by the client was terminated
        DLabsError
            Something went wrong while trying to post stats
        """
        assert self._ses.closed is False, "Client session closed"

        if self.bot is None:
            raise NoBotError("Cannot post stats without a commands.Bot object")

        elif self._token is None:
            raise DLabsError("Cannot post stats without a Discord Bot Labs token")

        data: dict = {"token": self._token,
                      "server_count": str(len(self.bot.guilds)),
                      "shard_count": str(self.bot.shard_count)} if self._post_shard_count else {"token": self._token,
                                                                                                "server_count": str(len(
                                                                                                    self.bot.guilds))}

        res_ = await self._ses.post(f"https://bots.discordlabs.org/v2/bot/{self.bot.user.id}/stats",
                                    json=data)

        res = await res_.json()

        if str(res["error"]).lower() == "true":
            if "retry-after" in res:
                raise DLabsError(f"{res['message']} | Retry After: {res['retry-after']}")
            raise DLabsError(res["message"])

    async def _autopost_stats(self):
        """
        Automatically posts stats to the DLabs API by creating a background task on the passed in discord.py Bot.
        The :class:`DLabsError` exception is excepted and printed to prevent an unexpected crash.

        Raises
        ------
        AssertionError
            The HTTP session used by the client was terminated
        """
        assert self._ses.closed is False, "Client session closed"

        await self.bot.wait_until_ready()

        while True:
            try:
                self._v("Posting stats to the DLabs API...")
                await self.post_stats()
                self._v("Successfully posted stats to the DLabs API")
                await sleep(1800)
            except DLabsError as e:
                print("Exception occurred when autoposting stats: ", e)

    async def close(self):
        """
        Closes the HTTP session.

        Raises
        ------
        AssertionError
            The HTTP session used by the client was terminated
        """
        assert self._ses.closed is False, "Client session already closed"

        self._v("Closing...")

        if self._autopost_task is not None:
            await self._autopost_task.cancel()
        await self._ses.close()

        self._v("Closed.")

    def _v(self, s: str):
        """
        Prints if verbose is True

        Parameters
        ----------
        s: :class:`str` The message to print
        """
        if self._verbose:
            print(s)
