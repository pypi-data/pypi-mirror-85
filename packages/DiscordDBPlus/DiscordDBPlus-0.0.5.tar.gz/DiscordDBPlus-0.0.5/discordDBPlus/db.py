import discord

from .models import Data


class DiscordDB(object):
    """The Discord database client.

    Parameters
    ----------
    bot : discord.ext.commands.Bot
        An instance of discord.py Client or Bot representing your discord application.
    db_channel_id : int
        An integer representing ID of Discord channel you want to be used as database.

    """

    def __init__(self, bot, db_channel_id: int):
        self.__bot = bot
        self.__channel_id = db_channel_id

    @property
    def channel(self):
        """A property which returns an instance of ``discord.TextChannel`` which is being used as database."""
        return self.__bot.get_channel(self.__channel_id)

    async def set_channel(self, channel_id: int):
        """A method used to change the channel in which all of your data will be sent

        Parameters:
        -----------
        channel_id : int
            Id of the channel you wish to change to.
        """
        self.__channel_id = channel_id

    async def save(self, data: dict) -> int:
        """A method to post and save data to your database channel.

        Parameters
        ----------
        data : dict
            Dictionary representing your raw data.

        Returns
        -------
        int
            An special integer which should be saved by the client to get this same data later.

        """
        embed = discord.Embed.from_dict({
            "fields": [{
                "name": name, "value": value
            } for name, value in data.items()]
        })
        message = await self.channel.send(embed=embed)
        return message.id

    async def saves(self, data: list) -> list:
        """A method used to post and save multiple data dict to a single channel.

        Parameters
        ----------
        data : list
            List of data dictionaries

        Returns
        -------
        list
            A list of ids
        """
        _data_list = []
        for _data in data:
            embed = discord.Embed.from_dict({
                "inline": True,
                "fields": [{
                    "name": name, "value": value
                } for name, value in _data.items()]
            })
            message = await self.channel.send(embed=embed)
            _data_list.append(message.id)
        return _data_list

    async def get(self, _id: int) -> dict:
        """A method used to get your saved data from the database channel.

        Parameters
        ----------
        _id : int
            An special integer which was received from the :py:meth:`discordDB.DiscordDB.set` method.

        Returns
        -------
        dict
            A dict containing the data recovered from the message.

        """
        message = await self.channel.fetch_message(_id)
        _data = message.embeds[0].to_dict()["fields"]
        data = {_["name"]: _["value"] for _ in _data}
        return data
    
    async def edit(self, _data: dict, _id: int):
        """A method used to edit a data message.
        You can use the get method to edit the Data dict then use this method to edit the embed.

        Parameters
        ----------
        _data : dict
            A dict containing the changes you want to make to the original message.

        _id : int
            The id of the message to edit.
        """
        message = await self.channel.fetch_message(_id)
        embed = discord.Embed.from_dict({
            "fields": [{
                "name": name, "value": value
            } for name, value in _data.items()]
        })
        await message.edit(embed=embed)
        