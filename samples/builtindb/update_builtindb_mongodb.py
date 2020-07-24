from datastore import MongoDB


def update_data_builtindb(event, context):
    augment_mongoclient = MongoDB()
    collection_name = "sample-collection-fauzan"
    data = event['data']
    old_data = {"name": data['old_name'], "company": data['old_company']}
    new_data = {"name": data['new_name'], "company": data['new_company']}
    try:
        update_result = augment_mongoclient.builtin_db[collection_name].replace_one(collection_name, old_data, new_data)
        if update_result.matched_count == 0:
            return "no matching data"
    except Exception as e:
        return str(e)
    result_data = update_result.raw_result
    result_data.pop('_id', None)

    return result_data
