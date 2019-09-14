print("In File: src/mdb_handling.py")

from flask_pymongo import PyMongo, MongoClient
from bson.objectid import ObjectId
from configs import db_config


class DbHandler:

    def open_collection(self, db_name: str, collection_name: str):
        client = MongoClient(db_config.connection_string)
        db = client.get_database(db_name)
        collection = db[collection_name]

        return client, collection

    def write_to_database(self, db_name: str, collection_name: str, json_to_write: dict) -> dict:
        print('In Method: write_to_database()')

        client, collection = self.open_collection(db_name, collection_name)

        try:
            doc_id = collection.insert_one(json_to_write)
        except Exception as e:
            print("Exception Thrown:")
            print(e)

            client.close()

            return {'success': False}

        client.close()

        return {'success': True, 'doc_id': doc_id.inserted_id}

    def read_one_doc_by_id_from_database(self, db_name: str, collection_name: str, doc_id: str) -> dict:
        print("In Method: read_one_doc_by_id_from_database()")

        client, collection = self.open_collection(db_name, collection_name)

        try:
            result = collection.find_one({"_id": ObjectId(doc_id)})
            result['_id'] = str(result['_id'])
        except Exception as e:
            print("Exception Thrown:")
            print(e)

            client.close()

            return {'success': False}

        client.close()

        return {'success': True, 'result': result}
