import json
from datastore import MongoDB

def list_data_builtindb(event, context):
    augment_mongoclient = MongoDB()
    collection_name = "sample-collection"
    try:
        get_data = augment_mongoclient.builtin_db[collection_name].find()
    except Exception as e:
        return str(e)
    find_value = []
    if get_data is not None:
        for element in get_data:
            element.pop('_id', None)
            find_value.append(element)
    else:
        return "no data found"
    return_value = json.dumps(find_value, indent=4)
    return return_value
