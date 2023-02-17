from berkeleydb import db
import json, os
from helpers import yes_or_no
import importlib
from bdb import BDB


class ConfigMan(BDB):

    def __init__(self, file_name):
        super().__init__(file_name)
        self.root = None
        self.configs = None
        self.sub_config = None
        self.cursor = None
        self.reinit()

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

    def create(self):
        print("Create function")
        if self.cursor[-1] == self.root:
            self.create_config()
            self.reinit()

    def create_config(self):
        print("Creating config ...")
        name = input("Input config name : ")
        print("You can load config template from config file")
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

        print("=" * 100)
        print("MENU : ", self.cursor[-1:][0])
        print("=" * 100)
        act_keys = {"C": {"cmd": self.create, "descr": "Create new"},
                    "F": {"cmd": self.fill, "descr": "Fill one"},
                    "D": {"cmd": self.delete, "descr": "Delete one"},
                    "S": {"cmd": self.show, "descr": "Show element"},
                    "B": {"cmd": self.back, "descr": f"Back to "},
                    "E": {"cmd": self.exit, "descr": "Exit program"}
                    }
        # Print act menu
        act_menu = []
        for act_key in act_keys:
            letter = list(act_key)[0]
            if (letter == "B" or letter == "D") and len(self.cursor) <= 1:
                continue
            if letter == "F" and "_template" not in self.sub_config:
                continue

            act_menu.append(letter)
            print(f"[ {letter} ] - {act_keys[act_key]['descr']}")
        print("=" * 100)

        # Print menu
        menu_list = []
        for key, val in self.sub_config.items():
            if isinstance(val, list) or isinstance(val, dict):
                menu_list.append(key)

        for idx, item in enumerate(menu_list):
            print(f"[ {idx} ] - {item}")

        print("=" * 100)
        select = input("Enter your select:")

        if select.isdigit() and select.isnumeric():
            if int(select) not in range(0, len(menu_list)):
                print("Incorrect select! Please try one more time.")
            else:
                self.cursor.append(menu_list[int(select)])
                self.get_sub_config()
            return self.menu()

        select = select.upper()
        if select not in act_menu:
            print("Incorrect select! Please try one more time.")
            return self.menu()

        act_keys[select]["cmd"]()
        #cmd = "self. " + act_keys[select]["cmd"] + "()"
        #eval(cmd)

        return self.menu()

    def __delete__(self, instance):
        self.DB.close()


if __name__ == '__main__':
    CM = ConfigMan("config_d.db")
    CM.DB.put("main3".encode(), json.dumps({"sada34{}": {"gssdsdsdsd": "hjhjskl;sk"}}).encode())
    print(CM.configs)
    CM.menu()
