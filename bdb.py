#!/bin/python
from berkeleydb import db
import json


class BDB:

    def __init__(self, file_name):
        self.DB = db.DB()
        self.DB.open(file_name, None, db.DB_HASH, db.DB_CREATE)
        self.curDB = self.DB.cursor()

    @staticmethod
    def bin_to(_bin):
        obj = _bin.decode()
        try:
            obj = json.loads(obj)
        except ValueError:
            print(obj, "is not json")
        return obj

    def read_all_db(self):
        print("Reading all DB")
        record = self.curDB.first()
        obj = {}
        while record:
            key = self.bin_to(record[0])
            val = self.bin_to(record[1])
            obj[key] = val
            record = self.curDB.next()
        print("All DB", json.dumps(obj, indent=4))
        return obj

    @staticmethod
    def to_bin(obj):
        if not isinstance(obj, str):
            obj = json.dumps(obj)
        return obj.encode()

    def add_db(self, record: dict):
        print("Adding new record to DB...")
        print(record)
        key = list(record.keys())[0]
        self.DB.put(self.to_bin(key), self.to_bin(record[key]))

    def delete_db(self, key):
        self.DB.delete(self.to_bin(key))
