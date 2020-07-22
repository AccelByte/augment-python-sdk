from datastore import BuiltInDB


def delete_data_builtindb(event, context):
    builtindb = BuiltInDB()
    collection_name = "sample-collection"
    data = event['data']
    created_data = builtindb.database.insert(collection_name, data)
    print(created_data)

    builtindb.database.delete(collection_name, created_data)
    return "ok"
