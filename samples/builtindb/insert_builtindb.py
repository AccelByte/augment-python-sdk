from datastore import BuiltInDB


def insert_data_builtindb(event, context):
    builtindb = BuiltInDB()
    collection_name = "sample-collection"
    data = event['data']
    try:
        created_data = builtindb.insert(collection_name, data)
        print(created_data)
    except Exception as e:
        return str(e)

    return created_data
