#!/bin/python
import sqlite3


class ConfigDB:

    def __init__(self, file_name):
        self.conn = sqlite3.connect(file_name)
        self.cur = self.conn.cursor()

    def get(self):
        pass

    def edit(self):
        pass

    def insert(self, table, name, data):
        query = f"""INSERT INTO {table} (name, data) VALUES(?, ?)"""
        self.cur.execute(query, (name, data))
        self.conn.commit()

    def create_key_table(self, table_name):
        self.cur.execute(f"""CREATE TABLE IF NOT EXISTS {table_name}(
                                id INTEGER PRIMARY KEY NOT NULL UNIQUE,
                                name TEXT NOT NULL UNIQUE,
                                data BLOB); """)


if __name__ == '__main__':
    page = ConfigDB("config.db")
    # page.create_key_table("pages")
    name = input("Enter page name")
    config_structure = {
        "URL": "",
        "OBJECT": {
            "_object_name": [
                {
                    'by': '',
                    'attr': '',
                    'many': '',
                    'position': ''
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
