from datastore import MongoDB


def get_data_builtindb(event, context):
    augment_mongoclient = MongoDB()
    collection_name = "sample-collection"
    data = event['data']
    try:
        get_data = augment_mongoclient.builtin_db[collection_name].find_one(data)
    except Exception as e:
        return str(e)
    if get_data is not None:
        get_data.pop('_id', None)
    else:
        return "data not found"

    return get_data
