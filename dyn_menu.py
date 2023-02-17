#!/bin/python

class DynMenu:
    def __init__(self, name, objects=None):
        self.name = name
        self.objects = [] if objects is None else objects
        self.description = ""

    def add_obj(self, obj):
        self.objects.append(obj)


    def activate(self):
        print("=" * 100)
        print("MENU : ", self.name)
        print("=" * 100)

        for menu in self.objects:
            if isinstance(menu, dict):
                self.print_dict(menu)

        select = input("Enter your select:")

    def print_dict(self, obj):
        print(obj)
        for key, val in obj.items():
            if key.lower() == "dev":
                print(val)
                continue
            if "hide" in val and val["hide"]:
                continue
            print(f"[ {key} ] - {val['descr'] if 'descr'in val else ''}")




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