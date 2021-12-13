from pycord import discord

class commandContext:

    def __init__(self, message: discord.Message = None, bot=None, member:discord.Member = None, **kwargs):

        if member == None: member = message.author

        self.message = message or None
        self.member = member
        self.bot = bot
        self.args = kwargs.pop("args") or None

        if(self.message is not None):
            self.guild = message.guild

        if(kwargs.keys().__contains__("slash_command_context")):
            self.slash_command_context = kwargs.pop("slash_command_context")

    @classmethod
    def slash_command_context_converter(cls,ctx, bot, args=None, **kwargs):
        """
        Creates a commandContext object from slash command context
        :param ctx:
        :param bot:
        :param args:
        :param kwargs:
        :return cls: An intance of the commandContext class
        """

        if("member" in kwargs.keys()):
            return cls(member=kwargs.pop("member"), bot=bot, args=args, slash_command_context=ctx)

        return cls(member=ctx.author, bot=bot, args=args, slash_command_context=ctx)

    def getMember(self):
        return self.member

    async def send(self, message=None, embed=None):
        """
        Implements the ability to send messages directly from the context object
        :param message: String
        :param embed: discord.Embed object
        :return: None
        """
        if(self.message is None):

            if(message is None and embed is None):
                return

            await self.slash_command_context.send(message, embed=embed)
            return

        if(embed is not None):

            if(message is not None):
                await self.message.channel.send(message, embed=embed)
                return

            await self.message.channel.send(embed=embed)

        if(message is not None):
            await self.message.channel.send(message)

