from datastore import BuiltInDB


def get_data_builtindb(event, context):
    builtindb = BuiltInDB()
    collection_name = "sample-collection"
    data = event['data']
    created_data = builtindb.database.insert(collection_name, data)
    print(created_data)

    get_data = builtindb.database.get(collection_name, created_data)
    return get_data
