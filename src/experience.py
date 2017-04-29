from pymongo import MongoClient
from multiprocessing import Process
import subprocess
import pprint
import os
import shutil

import config

class Experience:
    def __init__(self):
        self.mongo = Process(target=Experience.__start_mongo_server__, args=())
        self.mongo.start()
        self.client = MongoClient()
        self.db = self.client["wazuhl"]
        self.approved = self.db["approved"]
        self.waiting = self.db["waiting"]

    @staticmethod
    def __start_mongo_server__():
        dbpath = config.get_mongodb()
        subprocess.call(["mongod", "--dbpath", dbpath])

    def fill_records(self, value):
        new_records = []
        for item in self.waiting.find():
            record = {}
            record["state"] = item["state"]
            record["values"] = item["values"]
            record["values"][item["index"]] = value
            new_records.append(record)
        self.approved.insert_many(new_records)

if __name__ == "__main__":
    config.set_wd("/home/sin/binaries/wazuhl/")
    dbpath = config.get_mongodb()
    if not os.path.exists(dbpath):
        os.makedirs(dbpath)
    experience = Experience()
    dummy = [{"state": [1, 0],
              "values": [0.1, 0.2, 0.3]},
             {"state": [2.1, 1.5],
              "values": [42.1, 15.1, 11.1]},
             {"state": [32.1, 4.2],
              "values": [12.1, 45.6, 17]}]
    experience.approved.insert_many(dummy)
    dummy_waiting = [{"state": [32, 23],
                      "values": [1.0, 2.0, 5.0],
                      "index": 2},
                     {"state": [72, 12.1],
                      "values": [42.2, 41.1, 40.0],
                      "index": 0},
                     {"state": [13.3, 12.2],
                      "values": [3.0, 2.2, 99.9],
                      "index": 1}]
    experience.waiting.insert_many(dummy_waiting)
    experience.fill_records(178.41)
    for item in experience.approved.find():
        print item["values"]
        pprint.pprint(item)
    experience.mongo.terminate()
    shutil.rmtree(dbpath)
