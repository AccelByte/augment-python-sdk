from datastore import BuiltInDB


def get_data_builtindb(event, context):
    builtindb = BuiltInDB()
    collection_name = "sample-collection"
    data = event['data']
    try:
        get_data = builtindb.get(collection_name, data)
    except Exception as e:
        return str(e)
    return get_data
