print("In File: src/mdb_handling.py")

from flask_pymongo import PyMongo, MongoClient
from configs import db_config

class db_handler:    
    def write_to_database(self, db_name : str, collection_name : str, json_to_write : str) -> bool:
        print("In Method: write_to_database()")

        client = MongoClient(db_config.connection_string)
        db = client.get_database(db_name)
        collection = db[collection_name]

        try:
            collection.insert_one(json_to_write)
        except Exception as e:
            print("Exception Thrown:")
            print(e)

            client.close()

            return False

        client.close()

        return True