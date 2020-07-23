from datastore import BuiltInDB


def delete_data_builtindb(event, context):
    builtindb = BuiltInDB()
    collection_name = "sample-collection"
    data = event['data']
    try:
        builtindb.delete(collection_name, data)
    except Exception as e:
        return str(e)

    return "ok"
