#!/bin/python

class DynMenu:
    def __init__(self, name, objects=None):
        self.name = name
        self.objects = [] if objects is None else objects
        self.description = ""
        self.active_positions = {}
        self.selected = None

    def add_obj(self, obj):
        self.objects.append(obj)

    def clear(self):
        self.objects = []
        self.active_positions = {}
        self.selected = None

    def activate(self):
        self.selected = None
        print("=" * 100)
        print("MENU : ", self.name)
        print("=" * 100)

        for menu_obj in self.objects:
            if isinstance(menu_obj, dict):
                self.print_dict(menu_obj)
            print("-" * 100)

        self.select_position()
        return self.selected

    def select_position(self):
        select = input("Enter your select:").upper()
        if select not in self.active_positions:
            print("Incorrect select! Please try one more time.")
            return self.select_position()
        self.selected = self.active_positions[select]
        self.selected["key"] = select

    def print_dict(self, obj):
        for key, val in obj.items():
            if isinstance(key, str) and key.lower() == "dev":
                print(val)
                continue
            if "hide" in val and val["hide"]:
                continue
            self.active_positions[str(key)] = val
            print(f"[ {key} ] - {val['descr'] if 'descr' in val else ''}")


if __name__ == '__main__':
    act_keys = {
        "C": {"cmd": "create", "descr": "Create new"},
        "F": {"cmd": "fill", "descr": "Fill one"},
        "D": {"cmd": "delete", "descr": "Delete one"},
        "S": {"cmd": "self.show", "descr": "Show element"},
        "dev": "-" * 100,
        "B": {"cmd": "self.back", "descr": f"Back to "},
        "E": {"cmd": "self.exit", "descr": "Exit program"},

    }
    menu = DynMenu("menu name")
    menu.add_obj(act_keys)
    menu.activate()
