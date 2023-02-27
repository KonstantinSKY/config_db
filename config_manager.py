#!/bin/python
from config_db import ConfigDB
import os.path
import importlib
import json
from helpers import yes_or_no


class ConfigManager(ConfigDB):
    def __init__(self, file_name):
        super().__init__(file_name)
        self.record = ""
        self.block = ""
        self.configs = self.get_configs()
        self.cursor = self.configs


    def create_configs(self):

        print("Creating config")
        name = input("Input config name : ")
        file_name = input("Input config structure template . py file: ")
        structure = ""
        if file_name and os.path.isfile(file_name):
            module = importlib.import_module(file_name.rstrip(".py"))
            print("New config structure for: ", name)
            structure = module.STRUCTURE
            print(json.dumps(structure, indent=4))
            pass
        if not yes_or_no("Do your want to create config and to add it to DB?"):
            return
        self.add_config_db(name, json.dumps(structure))
        #CREATE_condfig
        # Create config record

        # Create config table
        # Reload self.config
    def menu(self):
        print("=" * 100)
        print("MENU : ", "Configs" if not self.cursor else self.cursor.keys()[0])
        print("=" * 100)
        print("[C] - Create new ")
        print("[S] - Show all")
        print("[E] - Exit")
        print("=" * 100)

        for idx, item in enumerate(list(self.cursor)):
            print(f"[ {idx} ] - {item}")
        #if not self.configs:
         #   return

        print("=" * 100)
        select = input("Enter your select:")

        self.cursor = self.configs[list(self.configs)[int(select)]]
        print(self.cursor)
        return self.menu()
        #eval("self.create_" + self.cursor + "()")
        #print("=CREATING CONFIG" * 200)

if __name__ == '__main__':
    CM = ConfigManager("config.db")
    configs = CM.configs
    print(CM.configs)
    print(CM.cursor)
    CM.menu()
    # records = CM.get_records()
    # menu
    """exit;
        create new config
        edit config
        list of configs
        
        
        
        """
