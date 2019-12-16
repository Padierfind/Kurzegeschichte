print("In File: src/authentication.py")

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from src.db_handling import DbHandler


class User(UserMixin):

    def __init__(self, user_id: str = 'not initialized', email: str = 'not initialized',
                 password: str = 'not initialized'):
        print("In Method: __init__()")

        self.user_id = user_id
        self.id = email
        self.password = password

    def sign_up(self):
        print("In Method: sign_up()")

        user_dict = {
            'user_id': self.user_id,
            'email': self.id,
            'password': generate_password_hash(self.password)
        }

        handler = DbHandler()
        db = 'production'
        collection = "users"
        result_of_db_operation = handler.write_to_database(db_name=db, collection_name=collection,
                                                           json_to_write=user_dict)

        if result_of_db_operation['success'] is True:
            return True
        else:
            return False

    def check_if_user_exists(self):
        print("In Method: check_if_user_exists()")

        handler = DbHandler()
        db = 'production'
        collection = 'users'
        result_of_db_operation = handler.read_one_doc_by_param_from_database(db_name=db, collection_name=collection,
                                                                             doc_value=self.id, doc_param='email')
        if result_of_db_operation['success'] is True:
            return result_of_db_operation
        else:
            return False

    def check_password(self, saved_password: str, input_password: str):
        print("In Method: check_password()")

        is_correct_password = check_password_hash(saved_password, input_password)

        return is_correct_password
