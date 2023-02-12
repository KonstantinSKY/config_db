from berkeleydb import db
import json


class ConfigMan:

    def __init__(self, db_name):
        self.DB = db.DB()
        self.DB.open(db_name, None, db.DB_HASH, db.DB_CREATE)
        self.curDB = self.DB.cursor()
        self.root = "Configs"
        self.configs = {self.root: self.read_db()}
        self.sub_config = self.configs[self.root]
        self.cursor = list(self.configs.keys())
        print("self.cursor", self.cursor)

    @staticmethod
    def bin_to(_bin):
        obj = _bin.decode()
        try:
            obj = json.loads(obj)
        except ValueError:
            print(obj, "is not json")
        return obj

    def read_db(self):
        record = self.curDB.first()
        configs = {}
        while record:
            print("Record:", record)
            key = self.bin_to(record[0])
            val = self.bin_to(record[1])
            configs[key] = val
            record = self.curDB.next()
        return configs

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
        act_keys = {"C": {"cmd": "create", "descr": "Create new"},
                    "B": {"cmd": "back", "descr": "Back to "},
                    "E": {"cmd": "exit", "descr": "Exit program"}
                    }
        # Print act menu
        act_menu = []
        for act_key in act_keys:
            letter = list(act_key)[0]
            if letter == "B" and len(self.cursor) <= 1:
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

        cmd = "self. " + act_keys[select]["cmd"] + "()"
        eval(cmd)
        return self.menu()

    def __delete__(self, instance):
        self.DB.close()


if __name__ == '__main__':
    CM = ConfigMan("config_d.db")
    CM.DB.put("main3".encode(), json.dumps({"sada34{}": {"gssdsdsdsd": "hjhjskl;sk"}}).encode())
    print(CM.configs)
    CM.menu()
