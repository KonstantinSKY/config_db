#!/bin/python
import sqlite3
import json

class ConfigDB:

    def __init__(self, file_name):
        self.conn = sqlite3.connect(file_name)
        self.cur = self.conn.cursor()

    def get_configs(self):
        results = self.cur.execute(f"""SELECT table_name, structure FROM Configs""").fetchmany()
        print(results)
        conf = {}
        for result in results:
            conf[result[0]] = {"structure": result[1]}

        return conf

        # if not res:
        #     return None
        # print(res)


    def get_records(self):
        pass


    def get(self):
        pass

    def edit(self):
        pass

    def add_config_db(self, name, structure):
        self.insert("Configs", {"table_name": name, "structure": structure})
        self.create_records_table(name)

    def insert(self, table, data):
        fields = ", ".join(list(data.keys()))
        print(fields)
        marks = "?, " * len(data)
        query = f"""INSERT INTO IF NOT EXISTS {table} ({fields}) VALUES({marks.rstrip(", ")})"""
        print(query)
        print(data.values())
        self.cur.execute(query, tuple(data.values()))
        self.conn.commit()

    def create_records_table(self, table_name):
        self.cur.execute(f"""CREATE TABLE IF NOT EXISTS {table_name}(
                                id INTEGER PRIMARY KEY NOT NULL UNIQUE,
                                name TEXT NOT NULL UNIQUE,
                                data BLOB); """)
    def create_config(self, name):
        pass

if __name__ == '__main__':
    page = ConfigDB("config.db")
    # page.create_key_table("pages")
    #name = input("Enter page name")
    config_structure = {
        "URL": "",
        "OBJECT": {
            "_object_name": [
                {
                    'by': '',
                    'attr': '',
                    'many': '',
                    'position': '',
                }]
        },
        "ACTIONS": {
            "_actions_name": [
                {
                    'obj': '',
                    'cmd': '',
                    'data': '',
                }
            ]
        },

    }
    """
    def show_config(page):
        pass
    def insert_block("object name")
        pass
    def find_blocks(structere)
        self.blocks

        #
        #TODO
        create new page
        show pages
        show page


        self.config = "main"
        self.block = "OBJECT"
            create new sub_block
            add.atributes
            edit
                find key
                select menu
            delete


    print(json.dumps(config_structure,  indent=4))
    print(type(config_structure))
    for key, val in config_structure.items():
        print(key)
        print(type(val))
        if isinstance(val, str):
            config_structure[key] = input(f"Input {key} :")

        # print(structure)
        # print(type(structure))
        # # print((config_structure[structure]))
        # print(type(config_structure[structure]))

    print(json.dumps(config_structure, indent=4))
"""