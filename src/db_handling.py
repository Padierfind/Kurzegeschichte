print('In File: src/mdb_handling.py')

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
            print('Exception Thrown:')
            print(e)

            client.close()

            return {'success': False}

        client.close()

        return {'success': True, 'doc_id': doc_id.inserted_id}

    def read_one_doc_by_id_from_database(self, db_name: str, collection_name: str, doc_id: str) -> dict:
        print('In Method: read_one_doc_by_id_from_database()')

        client, collection = self.open_collection(db_name, collection_name)

        try:
            result = collection.find_one({'_id': ObjectId(doc_id)})
            result['_id'] = str(result['_id'])
        except Exception as e:
            print('Exception Thrown:')
            print(e)

            client.close()

            return {'success': False}

        client.close()

        return {'success': True, 'result': result}

    def delete_from_all_collections_by_user_id(self, db_name: str, user_id: str) -> dict:
        print('In Method: delete_by_user_id()')

        client = MongoClient(db_config.connection_string)
        db = client.get_database(db_name)

        try:
            collection_names = [collection for collection in db.collection_names() if not collection.startswith('system.')]
            for collection_name in collection_names:
                db[collection_name].delete_many({'user_id': user_id})
        except Exception as e:
            print('Exception Thrown:')
            print(e)

            client.close()

            return {'success': False}

        client.close()

        return {'success': True}

    def read_one_doc_by_param_from_database(self, db_name: str, collection_name: str,
                                            doc_value: str, doc_param: str) -> dict:
        print('In Method: read_one_doc_by_param_from_database()')

        client, collection = self.open_collection(db_name, collection_name)

        dict_to_find = {
            doc_param: doc_value
        }

        try:
            result = collection.find_one(dict_to_find)
            result['_id'] = str(result['_id'])
        except Exception as e:
            print('Exception Thrown:')
            print(e)

            client.close()

            return {'success': False}

        client.close()

        return {'success': True, 'result': result}

    def read_multiple_docs_by_param_from_database(self, db_name: str, collection_name: str, doc_value: str,
                                                  doc_param: str) -> dict:
        print('In Method: read_one_doc_by_param_from_database()')

        client, collection = self.open_collection(db_name, collection_name)

        dict_to_find = {
            doc_param: doc_value
        }

        try:
            result = collection.find(dict_to_find)

            total_length = result.count()

            result_as_dict = []
            for x in result:
                result_as_dict.append(x)

            for obj in result_as_dict:
                obj['_id'] = str(obj['_id'])
        except Exception as e:
            print('Exception Thrown:')
            print(e)

            client.close()

            return {'success': False}

        client.close()

        return {'success': True, 'result': result_as_dict, 'total_length': total_length}

    def read_document_previews(self, db_name: str, collection_name: str, starting_id: int, amount_of_documents: int,
                               categories: list, lengths: list) -> dict:
        print('In Method: read_document_previews()')

        client, collection = self.open_collection(db_name, collection_name)

        try:
            if len(categories) != 0:
                categories_query = {'categories': {'$in': categories}}

            if len(lengths) != 0:
                lengths_query = {'length': {'$in': lengths}}

            query = {}

            if len(categories) != 0 and len(lengths) != 0:
                query = {'$and': [categories_query, lengths_query]}
            elif len(categories) == 0 and len(lengths) != 0:
                query = lengths_query
            elif len(categories) != 0 and len(lengths) == 0:
                query = categories_query

            print(query)
            result = collection.find(query).sort('{$natural:-1}').limit(amount_of_documents).skip(starting_id)
            total_length = result.count()

            result_as_dict = []
            for x in result:
                result_as_dict.append(x)

            for obj in result_as_dict:
                obj['_id'] = str(obj['_id'])

        except Exception as e:
            print('Exception Thrown:')
            print(e)

            client.close()

            return {'success': False}

        client.close()

        return {'success': True, 'result': result_as_dict, 'total_length': total_length}
