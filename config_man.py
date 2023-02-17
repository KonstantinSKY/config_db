from berkeleydb import db
import json, os
from helpers import yes_or_no
import importlib
from bdb import BDB
from dyn_menu import DynMenu


class ConfigMan(BDB):

    def __init__(self, file_name):
        super().__init__(file_name)
        self.root = None
        self.configs = None
        self.sub_config = None
        self.cursor = None
        self.reinit()
        self.main_menu = DynMenu("MENU")

    def reinit(self):
        self.root = "Configs"
        self.configs = {self.root: self.read_all_db()}
        self.sub_config = self.configs[self.root]
        self.cursor = list(self.configs.keys())
        print("self.cursor", self.cursor)

    def get_sub_config(self):
        self.sub_config = self.configs[self.root]
        print(self.cursor)
        if len(self.cursor) <= 1:
            return
        for key in self.cursor[1:]:
            print("Check key:", key)
            self.sub_config = self.sub_config[key]
        print(self.sub_config)

    def select_type(self):
        variants = {"1": {"cmd": "", "descr": "String"},
                    "2": {"cmd": [], "descr": "[] List or Array"},
                    "3": {"cmd": {}, "descr": "{} Dictionary or hash"}
                    }

    def sub_menu(self, variants):
        for key, val in variants.items():
            print(f"[{key}] - {val['descr']}")

        select = input("Enter your select: ")
        if select not in variants:
            print("Incorrect select! Please try one more time.")
            self.sub_menu(variants)
        else:
            return variants[select]

        print("Select structure type:")

    def empty(self):
        print("Select type structure of your config"

              )

    def create(self):
        print("Create function")
        if self.cursor[-1] == self.root:
            self.create_config()
            self.reinit()

    def create_config(self):
        print("Creating config ...")
        name = input("Input config name : ")
        print("You can load config template from config file")

        # if yes_or_no(f"Do your want to create {name} element from config file?"):
        #     self.empty()
        #     self.add_db(self.config)

        print("config json structure inside the file must have the same name like config:", name)
        file_name = input("Input config structure template .py file: ")
        config = {name: {}}
        if not file_name or not os.path.isfile(file_name):
            print("Wrong file name:", file_name)
            if yes_or_no("Do your want to create config without template with empty {} and to add it to DB?"):
                self.add_db(config)
            return

        module = importlib.import_module(file_name.rstrip(".py"))
        if not hasattr(module, name):
            print("The config file does not contain root structure: ", name)
            print(module.__dir__())
            if yes_or_no("Do your want to create config without template with empty {} and to add it to DB?"):
                self.add_db(config)
            return

        print(config)
        print(getattr(module, name))
        # config[name] = {"template": module.name}
        print("New template for :", name)
        obj = getattr(module, name)
        print(json.dumps(obj, indent=4)) if isinstance(obj, dict) or isinstance(obj, list) else obj
        if not yes_or_no("Do your want to create config with template and add it to DB?"):
            return
        config[name]["_template"] = getattr(module, name)
        print(config[name])
        self.add_db(config)

    def fill(self):
        print("Filling config thru template")
        print(self.sub_config)
        template = self.sub_config["_template"]
        print("template", template)
        if isinstance(template, dict):
            for key, val in template.items():
                print(key[0])
                if key[0] == "_":
                    sub_name = key[1:]
                    print(sub_name)
                    key_name = input("Enter ", sub_name)

        # if isinstance(template, list):

    def delete(self, key):
        pass

    def show(self):
        print("Element", self.cursor[-1], "structure:")
        print(self.cursor[-1], " = ", json.dumps(self.sub_config, indent=2))

    def back(self):
        self.cursor.pop()
        self.get_sub_config()

    def exit(self):
        print("Exiting program")
        self.DB.close()
        exit()

    def menu(self):
        self.main_menu.name = self.cursor[-1:][0]
        act_keys = {"C": {"cmd": self.create, "descr": "Create new"},
                    "F": {"cmd": self.fill, "descr": "Fill one"},
                    "D": {"cmd": self.delete, "descr": "Delete one"},
                    "S": {"cmd": self.show, "descr": "Show element"},
                    "B": {"cmd": self.back, "descr": f"Back to "},
                    "E": {"cmd": self.exit, "descr": "Exit program"}
                    }
        for key, val in act_keys.items():
            if (key == "B" or key == "D") and len(self.cursor) <= 1:
                act_keys[key]["hide"] = True
                continue
            if key == "F" and "_template" not in self.sub_config:
                act_keys[key]['hide'] = True
                continue

        self.main_menu.add_obj(act_keys)
        # Additional dynamic menu
        addition_menu = {}

        for idx, key in enumerate(self.sub_config.keys()):
            if isinstance(self.sub_config[key], list) or isinstance(self.sub_config[key], dict):
                addition_menu[str(idx)] = {"descr": str(key)}

        self.main_menu.add_obj(addition_menu)
        select = self.main_menu.activate()
        if "cmd" in select and callable(select["cmd"]):
            select["cmd"]()
        else:
            self.cursor.append(select['descr'])

        self.main_menu.clear()
        self.get_sub_config()
        return self.menu()

    def __delete__(self, instance):
        self.DB.close()


if __name__ == '__main__':
    CM = ConfigMan("config_d.db")
    CM.DB.put("main3".encode(), json.dumps({"sada34{}": {"gssdsdsdsd": "hjhjskl;sk"}}).encode())
    print(CM.configs)
    CM.menu()
