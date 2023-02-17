#!/bin/python

class DynMenu:
    def __init__(self, name, objects=None):
        self.name = name
        self.objects = [] if objects is None else objects
        self.description = ""
        self.selected = None

    def add_obj(self, obj):
        self.objects.append(obj)

    def clear(self):
        self.objects = []
        self.selected = None

    def activate(self):
        self.selected = None
        print("=" * 100)
        print("MENU : ", self.name)
        print("=" * 100)

        for menu_obj in self.objects:
            if isinstance(menu_obj, dict):
                self.print_dict(menu_obj)
            print("=" * 100)
        if not self.select_position():
            print("Incorrect select! Please try one more time.")
            return self.activate()
        return self.selected

    def select_position(self):
        select = input("Enter your select:").upper()
        for menu_obj in self.objects:
            print(menu_obj)
            if select not in menu_obj:
                continue
            self.selected = menu_obj[select]
            self.selected["key"] = select
            return True
        return False

    def print_dict(self, obj):
        for key, val in obj.items():
            if isinstance(key, str) and key.lower() == "dev":
                print(val)
                continue
            if "hide" in val and val["hide"]:
                continue
            print(f"[ {key} ] - {val['descr'] if 'descr' in val else ''}")


if __name__ == '__main__':
    act_keys = {
        "C": {"cmd": "create", "descr": "Create new"},
        "F": {"cmd": "fill", "descr": "Fill one"},
        "D": {"cmd": "delete", "descr": "Delete one"},
        "S": {"cmd": "self.show", "descr": "Show element"},
        "dev": "=" * 100,
        "B": {"cmd": "self.back", "descr": f"Back to "},
        "E": {"cmd": "self.exit", "descr": "Exit program"},

    }
    menu = DynMenu("menu name")
    menu.add_obj(act_keys)
    menu.activate()
