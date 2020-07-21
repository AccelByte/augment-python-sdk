from datastore import BuiltInDB


def update_data_builtindb(event, context):
    builtindb = BuiltInDB()
    collection_name = "sample-collection"
    data = event['data']
    created_data = builtindb.database.insert(collection_name, data)
    print(created_data)

    new_data = data
    new_data["name"] = "updated_name"
    updated_data = builtindb.database.update(collection_name, created_data, new_data)
    return updated_data
