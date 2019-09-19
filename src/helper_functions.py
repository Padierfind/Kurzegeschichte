print("In File: src/helper_functions.py")

from bson.objectid import ObjectId


def recursive_list_convert_object_id_to_str(obj):
    print('In Method: RecursiveChildConvertion()')
    print(obj[0])
    new_child_list = []
    for child_x in range(0, len(obj)):
        print(child_x)
        if isinstance(obj[child_x], list):
            print("IST LIST")
            recursive_list = recursive_list_convert_object_id_to_str(obj[child_x])
            new_child_list.append(recursive_list)
        elif isinstance(obj[child_x], dict):
            print("IST DICT")
            recursive_list = recursive_list_convert_object_id_to_str(obj[child_x])
            new_child_list.append(recursive_list)
            print("hallooo")
        elif isinstance(obj[child_x], ObjectId):
            print("OBJEKT ID ALARM")
            converted = str(obj[child_x])
            new_child_list.append(converted)
        else:
            print("IST NORMAL")
            print(type(obj[child_x]))
            new_child_list.append(obj[child_x])

    return new_child_list
