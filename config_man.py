import rich
from berkeleydb import db
import json, os
from helpers import yes_or_no
import importlib
from bdb import BDB
from dyn_menu import DynMenu
from rich import print_json
import readline

class ConfigMan(BDB):
# Todo Clone
# TODO Fill
#TODO refactor

    def __init__(s, file_name):
        super().__init__(file_name)
        s.root = "Config"
        s.configs = {s.root: s.read_all_db()}
        s.sub_config = s.configs[s.root]
        s.cursor = list(s.configs.keys())
        s.main_menu = DynMenu("MENU")

    def get_sub_config(s):
        s.sub_config = s.configs[s.root]
        if len(s.cursor) <= 1:
            return
        for key in s.cursor[1:]:
           # print("Check key:", key)
            s.sub_config = s.sub_config[key]

    def enter_name(self):
        return input(f"Input NEW {self.cursor[-1:][0].rstrip('s')} name : ")

    def save_active_config(s):
        s.add_db({s.cursor[1]: s.configs[s.root][s.cursor[1]]})

    def enter_name_clear(s):
        curs, root, sub_conf, confs = s.cursor, s.root, s.sub_config, s.configs

        name = s.enter_name()
        if curs[-1] == root:
            print(curs[-1], "must be only {} json or dictionary format, the object will be create automatically!")
            sub_conf[name] = {}
            s.add_db({name: {}})

        else:
            sub_conf[name] = s.select_type()
            s.save_active_config()
        print(sub_conf[name])
        if not (isinstance(sub_conf[name], dict) or isinstance(sub_conf[name], list)):
            return
        curs.append(name)
        s.get_sub_config()

    def update_name(self):
        pass

    def create(self):
        parent = self.cursor[-1:][0]

        print("Creating NEW", parent)
        # name = input(f"Input NEW {parent} name : ")

        create_menu_keys = {
            "N": {"cmd": self.enter_name_clear, "descr": f"Enter New {parent} : Name (or Key) + clear object"},
            "AT": {"cmd": self.add_templ, "descr": f"Add new template for config: {parent}"},
            "U": {"cmd": self.update_name, "descr": "Update template name and add template part to fill"},
            "T": {"cmd": self.add_templ, "descr": "Create from Template"},
            "C": {"cmd": self.select_type, "descr": "Create from Clear structure"},
            "B": {"cmd": self.update_name, "descr": "Back to previous menu"},

        }

        create_menu = DynMenu(f"MENU - Creating new {parent}")
        create_menu_keys["AT"]["hide"] = True if len(self.cursor) != 2 else False
        create_menu.add_obj(create_menu_keys)
        create_menu.activate()["cmd"]()
        return


    def add_templ(s):
        curs, sub_conf = s.cursor, s.sub_config

        file_name = input("Input config structure template .json file:")
        if not file_name or not os.path.isfile(file_name):
            print("Wrong file name:", file_name)
            return
        with open(file_name, "r") as f:
            template = json.load(f)

        print("Template :")
        print(json.dumps(template, indent=4))
        if not yes_or_no(f"Do you want to add to config : {curs}"):
            return
        sub_conf.update(template)
        s.save_active_config()
        s.get_sub_config()
        return

    @staticmethod
    def select_type():
        type_menu_keys = {
            "D": {"cmd": {}, "descr": "{dict} - Dictionary or hash"},
            "L": {"cmd": [], "descr": "[list -  List or array"},
            "S": {"cmd": "", "descr": '"str" - String'},
            "I": {"cmd": int(), "descr": "int() = 0 - Integer number"},
            "F": {"cmd": float(), "descr": "float() = 0.0 - Float number"},
            "N": {"cmd": None, "descr": "None"},
        }

        type_menu = DynMenu("MENU - type of config element  ")

        type_menu.add_obj(type_menu_keys)
        return type_menu.activate()["cmd"]

    def delete(s):
        curs = s.cursor
        print("!!!Deleting config element with all inside structure and data :", curs[1])
        s.show()
        if not yes_or_no(f"Do you want to delete : {curs[-1]} !!!???"):
            return
        elem = curs.pop()
        s.get_sub_config()
        del s.sub_config[elem]

        if len(curs) == 1:
            s.delete_db(elem)
        else:
            s.save_active_config()


    def fill(self):
        pass

    def show(self):
        print("Element", self.cursor[-1], "structure:")
        print(self.cursor[-1], ":")
        rich.print_json(json.dumps(self.sub_config))

    def back(self):
        self.cursor.pop()
        self.get_sub_config()

    def exit(self):
        print("Exiting program")
        self.DB.close()
        exit()

    @staticmethod
    def rlinput(prompt, prefill=''):
        readline.set_startup_hook(lambda: readline.insert_text(prefill))
        try:
            return input(prompt)
        finally:
            readline.set_startup_hook()

    @staticmethod
    def is_json(obj):
        try:
            obj = json.loads(obj)
        except ValueError:
            print(obj, "is not json")
        return obj


    def edit(self):
        print("Editing object :", self.cursor[-1])
        curr = self.cursor[-1]
        print("Edit object and push enter \n")
        new_obj = self.rlinput("", json.dumps(self.sub_config))
        new_obj = self.is_json(new_obj)
        print(new_obj)
        if not yes_or_no("Do you want to add this changes to D"):
            return self.edit() if not yes_or_no("Do you to cancel this edition?") else None

        self.cursor.pop()
        self.get_sub_config()
        self.sub_config[curr] = new_obj
        self.cursor.append(curr)

        self.get_sub_config()
        print(self.sub_config)
        print(self.configs)

        self.save_active_config()
        print(new_obj)

    def menu(s):
        curs, sub_conf = s.cursor, s.sub_config
        print(sub_conf)
        s.main_menu.name = f"{curs[-1]} {' ' * 20} {sub_conf}"
        act_keys = {"C": {"cmd": s.create, "descr": f"Create new object in {curs[-1]} "},
                    "T": {"cmd": s.add_templ, "descr": f"Add new template for config: {curs[-1]}", "hide": True},
                    "F": {"cmd": s.fill, "descr": "Fill one"},
                    "E": {"cmd": s.edit, "descr": "Edit object"},
                    "D": {"cmd": s.delete, "descr": "Delete one"},
                    "S": {"cmd": s.show, "descr": "Show object"},
                    "B": {"cmd": s.back, "descr": f"Back to "},
                    "Q": {"cmd": s.exit, "descr": "Exit program"}
                    }
        for key, val in act_keys.items():
            if (key == "B" or key == "D") and len(curs) <= 1:
                val["hide"] = True
                continue

            if key == "T" and len(curs) == 2 and "_template" not in sub_conf:
                val["hide"] = False
                continue

            if key == "F" and "_template" not in sub_conf:
                val['hide'] = True
                continue

        s.main_menu.add_obj(act_keys)
        # Additional dynamic menu
        addition_menu = {}

        if isinstance(sub_conf, dict):
            num = 1
            for key, config in sub_conf.items():
                print(config)
                if not (isinstance(config, list) or isinstance(config, dict)):
                    continue
                addition_menu[str(num)] = {"descr": key, "content": config}
                num += 1

        if isinstance(sub_conf, list):
            for idx, config in enumerate(sub_conf):
                if not (isinstance(config, list) or isinstance(config, dict)):
                    continue
                addition_menu[idx] = {"descr": config}

        s.main_menu.add_obj(addition_menu)
        select = s.main_menu.activate()

        if "cmd" in select and callable(select["cmd"]):
            select["cmd"]()
        else:
            if isinstance(sub_conf, dict):
                s.cursor.append(select['descr'])
            if isinstance(sub_conf, list):
                s.cursor.append(int(select['key']))

        s.main_menu.clear()
        s.get_sub_config()
        print(s.get_sub_config())
        return s.menu()

    def __delete__(self, instance):
        self.DB.close()


if __name__ == '__main__':
    print(DynMenu("test").__dir__())
    CM = ConfigMan("config_d.db")
    # CM.DB.put("main3".encode(), json.dumps({"sada34{}": {"gssdsdsdsd": "hjhjskl;sk"}}).encode())
    # print(CM.configs)
    CM.menu()
