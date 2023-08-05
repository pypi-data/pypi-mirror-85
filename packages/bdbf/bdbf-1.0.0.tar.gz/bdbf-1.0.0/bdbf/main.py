import discord
from bdbf.exceptions import *
from bdbf.functions import *
import typing
import asyncio
import logging

log = logging.getLogger(__name__)

class Client(discord.Client):
    r"""Discord client class inherited from discord.Client.
    This documentation covers only the changes. For the inherited
    functions please head to the `discord.py documentation <https://discordpy.readthedocs.io/en/latest/api.html#discord.Client>`_

    :param embedFooter: Optional[:class:`dict`]
        The footer of embeds.

    :param embedColor: Optional[:class:`tuple[int,int,int]`]
        The color of embeds.

    :param botName: Optional[:class:`str`]
        The name of the bot.

    :param commandPrefix: Optional[:class:`str`]
        The prefix of all commands.

    :param useDefaultHelp: Optional[:class:`bool`]
        Whether to use the default help.

    :param isHelpInline: Optional[:class:`bool`]
        If using the default help. Wheter it is inline or not.
    """
    def __init__(self, *, loop=None, **options):
        super().__init__(loop=loop, **options)
        self.commands = {}
        self.embedFooter = options.pop("embedFooter", {})
        self.embedColor = options.pop("embedColor", (0,0,0))
        self.botName = options.pop("botName", None)
        self.commandPrefix = options.pop("commandPrefix", None)
        self.logging = options.pop("logging", False)
        self.loggingFunction = None

        self.roleToReaction = {}

        if options.pop("useDefaultHelp", True):
            @self.command("help")
            async def help(msg):
                """Help"""
                fields = [(command, self.commands[command].__doc__, options.pop("isHelpInline", True)) for command in self.commands.keys()]
                e = self.embed(f"Help for {self.botName}", fields=fields)
                await msg.channel.send(embed=e)

        @self.event
        async def on_raw_reaction_add(payload):
            pass

        @self.event
        async def on_raw_reaction_remove(payload):
            pass
    
    def command(self, name, **options):
        r"""Wrapper fuction for making commands.
        Like ::

            @client.command("command")
            def command(message):
                print(message.content)"""
        def register(function):
            if name in self.commands.keys():
                raise CommandNameAlreadyRegistered(f"The command name {name} is already registered and can't be used again.")
            self.commands[name] = function
            log.debug(f"Function {function.__name__} has been registered for command {name}")
            return function
        return register

    async def tryCommand(self, msg, command, *options):
        try:
            if None not in options:
                try:
                    await self.commands[command](msg, *options)
                except:
                    await self.commands[command](msg)
            else:
                await self.commands[command](msg)
        except KeyError:
            pass

    async def useCommand(self, msg):
        message = msg.content
        if len(message) != 0:
            if message[:len(self.commandPrefix)] == self.commandPrefix:
                if len(message[len(self.commandPrefix):].split(" ", 1)) == 1:
                    cmd, args = message[len(self.commandPrefix):], None
                else:
                    cmd, args = message[len(self.commandPrefix):].split(" ", 1)[0], message[1:].split(" ",1)[1]
            else:
                cmd, args = None, None
        else:
            cmd, args = None, None

        await self.tryCommand(msg, cmd, args)

    def event(self, coro):
        r"""A decorator that registers an event to listen to.

        You can find more info about the events on the :ref:`documentation below <discord-api-events>`.

        The events must be a :ref:`coroutine <coroutine>`, if not, :exc:`TypeError` is raised.

        Example
        ---------

        .. code-block:: python3

            @client.event
            async def on_ready():
                print('Ready!')

        Raises
        --------
        TypeError
            The coroutine passed is not actually a coroutine.
        """
        if coro.__name__ == "on_message":
            async def on_message(msg, **options):
                a = await coro(msg, **options)
                if a == None:
                    a = {}
                if a.pop("command",True):
                    await self.useCommand(msg)
                if a.pop("log", True) and self.logging:
                    if self.loggingFunction != None:
                        if asyncio.iscoroutinefunction(self.loggingFunction):
                            await self.loggingFunction(msg)
                        else:
                            self.loggingFunction(msg)
                return a
            return super().event(on_message)

        elif coro.__name__ == "on_raw_reaction_add":
            async def on_raw_reaction_add(payload):
                a = await coro(payload)
                await self.tryReactionRole("add", payload)
                return a
            return super().event(on_raw_reaction_add)

        elif coro.__name__ == "on_raw_reaction_remove":
            async def on_raw_reaction_remove(payload):
                a = await coro(payload)
                await self.tryReactionRole("remove", payload)
                return a
            return super().event(on_raw_reaction_remove)


        return super().event(coro)

    async def tryReactionRole(self, a, payload):
        if a == "add":
            try:
                await payload.member.add_roles(discord.Object(self.roleToReaction[payload.message_id][payload.emoji.name]))
            except KeyError:
                pass
        elif a == "remove":
            try:
                await self.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(discord.Object(self.roleToReaction[payload.message_id][payload.emoji.name]))
            except KeyError:
                pass



    def logMessage(self, function):
        r"""Wrapper fuction for making a logging function.
        Like ::

            @client.logMessage
            def log(message):
                print(message.content)"""
        print("ahoj0")
        self.loggingFunction = function
        print("ahoj")
        log.debug(f"Function {function.__name__} has been registered as message logging function.")
        return function

    def reactionRole(self, msg, emoji, role):
        r"""Function to add reaction role functions to a message.
        
        :param msg: :class:`Union[discord.Message,int]`
            Message or message id of the message you want to add the reaction role functionality.
        :param emoji: :class:`str`
            Emoji. If a unicode emoji use it, if a custom emoji use it's name.
        :param role: :class:`int`
            Role id of the role you want to add to the emoji."""
        if type(msg) == discord.Message:
            msg = msg.id
        elif type(msg) != int:
            raise TypeError(f"Message has to be eighter int or discord.Message not {type(msg)}")
        
        self.roleToReaction[msg] = {emoji: role}

    def embed(self, title, **options):
        """Returns discord embed from given parameters with automatic footer and color options.

        :param title: :class:`str`
            Title of the embed
        :param url: :class:`Optional[str]`
            url of the title
        :param description: :class:`Optional[str]`
            Description of the embed
        :param fields: :class:`Optional[List[Tuple[str,str,Optional[bool]]]]`
            Fields of the embed.
            A tuple with item 1 being the name of the field, item 2 the value and item 3 weather is inline or not, item 3 is optional
        :param image: :class:`Optional[str]`
            Url of the embed image
        :param thumbnail: :class:`Optional[str]`
            Url of the thumbnail image
        :param author: :class:`Optional[Dict[str,str]]`
            Author of the embed
            
        :returns: :class:`discord.Embed`"""
        return embed(title,footer=self.embedFooter, color=self.embedColor, **options)
