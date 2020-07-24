from datastore import MongoDB


def insert_data_builtindb(event, context):
    augment_mongoclient = MongoDB()
    collection_name = "sample-collection"
    data = event['data']
    try:
        augment_mongoclient.builtin_db[collection_name].insert_one(data)
    except Exception as e:
        return str(e)
    data.pop('_id', None)

    return data
