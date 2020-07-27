from datastore import MongoDB


def delete_data_builtindb(event, context):
    augment_mongoclient = MongoDB()
    collection_name = "sample-collection"
    data = event['data']
    try:
        delete_result = augment_mongoclient.builtin_db[collection_name].delete_one(data)
        if delete_result.deleted_count == 0:
            return "data not found"
    except Exception as e:
        return str(e)

    return "ok"
