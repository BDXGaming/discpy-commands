import asyncio
import importlib
import os

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

    def get_command_names(self):
        return self.command_names

    async def register_commands(self):

        for file in os.listdir("./commandClasses"):
            name = file.title().lower()
            if(name.lower().__contains__(".py") and not name.__contains__("__init__")):
                print(name[:-3]+"."+name[:-3])
                thing = importlib.__import__("commandClasses."+name[:-3])
                met = getattr(thing, (name[:-3]).lower())
                self.add_command(met, name=name[:-3])
                self.command_names.append(name[:-3])

    def reload_command(self, command_name):
        for file in os.listdir("./commandClasses"):
            name = file.title().lower()
            if(name[:-3] == command_name):
                thing = importlib.__import__("commandClasses." + name[:-3])
                met = getattr(thing, (name[:-3]).lower())
                self.add_command(met, name=name[:-3])
                self.command_names.append(name[:-3])
                print("Command Reloaded")


    def add_command(self, meth, **kwargs):
        self.commands[kwargs["name"]] = meth

    def get_command(self, command_name):
        return self.commands[command_name]

