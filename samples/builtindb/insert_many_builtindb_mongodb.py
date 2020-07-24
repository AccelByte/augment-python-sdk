from datastore import MongoDB


def insert_many_data_builtindb(event, context):
    augment_mongoclient = MongoDB()
    collection_name = "sample-collection"
    data = event['data']
    try:
        augment_mongoclient.builtin_db[collection_name].insert_many(data)
    except Exception as e:
        return str(e)

    for element in data:
        element.pop('_id', None)

    return data
