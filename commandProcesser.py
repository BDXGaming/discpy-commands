from .commandManager import commandManager
from .commandContext import commandContext

class commandProcesser:

    instance = None

    def __init__(self, **kwargs):
        if(commandProcesser.instance == None):
            commandProcesser.instance = self

        if("prefixes" not in kwargs.keys()):
            self.prefixes = ["!c"]
        else:
            self.prefixes = kwargs.pop("prefixes")
            self.bot = kwargs.pop("bot")

    @staticmethod
    def getInstance():
        '''
        This method gets the instance of the commandProcesser which is active and returns it
        :return self: Instance of commandProcesser cls
        '''
        return commandProcesser.instance

    async def parse_string_to_args(self, message):
        args =  message.content.split(" ")
        args.pop(0)
        final_args, contains_member = await self.convert_args_to_member(args, self.bot, message.guild.id)
        return await self.clean_args(final_args), contains_member

    async def id_to_member(self, user_id:int, bot, guild_id=None, guild=None):
        '''
        Converts a user id to a member object
        :param user_id: the discord user id
        :param bot: the bot object
        :param guild_id: the id of the guild
        :param guild: The guild object
        :return: The member object
        '''
        if guild is None: guild = bot.get_guild(guild_id)

        return guild.get_member(user_id)

    async def convert_args_to_member(self, args, bot, guild_id):
        """
        Replaces any user id's or user pings with the discord.Member object
        :param args: the string[] of command args
        :param bot: discord.Bot
        :param guild_id: the guild id
        :return args: the updated args list
        """

        final_args = args
        contains_member = {"status":False}
        for index, arg in enumerate(args):
            user = None

            if arg.isdecimal() and len(arg) <=18:
                user = await self.id_to_member(int(arg), bot=bot, guild_id=guild_id)

            elif (arg.startswith("<@!") or arg.startswith("<@")):
                arg = arg[3:-1]
                user = await self.id_to_member(int(arg), bot=bot, guild_id=guild_id)

            if user is not None:
                final_args[index] = user
                contains_member = {"status":True, "index":index}

        return final_args, contains_member

    async def clean_args(self, args):
        """
        Cleans up the message args and removes any spaces that may still remain in the args
        :param args:
        :return cleaned_args:
        """
        cleaned_args = args
        for index, arg in enumerate(args):
            if arg == '':
                cleaned_args.pop(index)

        return cleaned_args

    async def process_message(self, bot, message):
        """
        This method takes a message object and processes the message for commands
        :param message: discord.Message
        :param bot: discord.Bot instance
        """

        prefix = None
        for _prefix in self.prefixes:
            if message.content.startswith(_prefix):
                prefix = _prefix
                break

        if prefix == None:
            return

        elif (message.content[len(prefix):len(prefix) + 5] == "whois"):
            command = "whois"

            if (len(message.content) > (len(prefix) + len(command))):
                guild = bot.get_guild(message.guild.id)

                if ("<@" in message.content):
                    member_id = message.content[(len(prefix) + len(command) + 4):-1]

                else:
                    member_id = message.content[(len(prefix) + len(command) + 1):]

                member = await self.id_to_member(int(member_id), bot, guild=guild)
                meth = commandManager.getInstance().get_command("whois")
                await message.channel.send(embed=(await meth(member)))

            else:
                meth = commandManager.getInstance().get_command("whois")
                await message.channel.send(embed=(await meth(message.author)))

        #Works for all commands which only need the bot instance
        else:

            for c in commandManager.getInstance().get_command_names():

                #Checks if commandManager contains a command with the given command name
                if(message.content[len(prefix):].startswith(c)):

                    #Processes the message as a command for args
                    args, contains_member = await self.parse_string_to_args(message)
                    if (contains_member["status"]):
                        ctx = commandContext(message, bot, args=args, member=args[contains_member["index"]])
                    else:
                        ctx = commandContext(message, bot, args=args)

                    #Gets the command method
                    meth = commandManager.getInstance().get_command(c)

                    #Calls the command method
                    result = await meth(ctx)

                    #If the command returns results are sent as String
                    if(result is not None): await message.channel.send(result)

                    break