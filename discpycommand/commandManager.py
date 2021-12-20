import asyncio
import importlib
import os

from .errors import CommandNotFound


class commandManager:
    commandManagerInstance = None

    def __init__(self):

        if(commandManager.commandManagerInstance == None):
            commandManager.commandManagerInstance = self
        else:
            print("Command Manager Instance already exists!")

        self.commands = {}
        self.command_names = []
        asyncio.get_event_loop().create_task(self.register_commands())

    @staticmethod
    def getInstance():
        '''
        This method gets the instance of the commandManager which is active and returns it
        :return self: Instance of commandManager cls
        '''
        return commandManager.commandManagerInstance

    @staticmethod
    def reset():
        commandManager.commandManagerInstance = None

    def get_command_names(self):
        return self.command_names

    async def register_commands(self):
        """
        Finds and registers all python files which can be used as commands in the commandClasses package.
        Calls the add_command() method and adds the command names to the command_names list
        :return:
        """
        for file in os.listdir("./commandClasses"):
            name = file.title().lower()
            if(name.lower().__contains__(".py") and not name.__contains__("__init__")):
                print(name[:-3]+"."+name[:-3])
                thing = importlib.import_module("commandClasses."+name[:-3])
                importlib.reload(thing)
                met = getattr(thing, (name[:-3]).lower())
                self.add_command(meth = met, name=name[:-3])
                self.command_names.append(name[:-3])

    async def reload_command(self, command_name):
        """
        Reloads the given command if the command exists
        :param command_name:
        :return:
        """
        if(command_name in self.command_names):

            for file in os.listdir("./commandClasses"):
                name = file.title().lower()
                if (name.lower().__contains__(".py") and name[:-3] == command_name):
                    print(name[:-3] + "." + name[:-3])
                    thing = importlib.import_module("commandClasses." + name[:-3])
                    importlib.reload(thing)
                    met = getattr(thing, (name[:-3]).lower())
                    self.add_command(meth = met, name=name[:-3])
                    self.command_names.append(name[:-3])
                    return

        raise CommandNotFound


    def add_command(self, **kwargs):

        if("meth" in kwargs.keys()):
            self.commands[kwargs["name"]] = kwargs.pop("meth")

    def get_command(self, command_name):
        return self.commands[command_name]

