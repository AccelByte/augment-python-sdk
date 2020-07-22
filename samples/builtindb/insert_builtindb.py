from datastore import BuiltInDB


def insert_data_builtindb(event, context):
    builtindb = BuiltInDB()
    collection_name = "sample-collection"
    data = event['data']
    created_data = builtindb.database.insert(collection_name, data)
    print(created_data)
    return created_data
