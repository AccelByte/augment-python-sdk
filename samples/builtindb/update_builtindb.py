from datastore import BuiltInDB


def update_data_builtindb(event, context):
    builtindb = BuiltInDB()
    collection_name = "sample-collection-fauzan"
    data = event['data']
    old_data = {"name": data['old_name'], "company": data['old_company']}
    new_data = {"name": data['new_name'], "company": data['new_company']}
    try:
        updated_data = builtindb.update(collection_name, old_data, new_data)
    except Exception as e:
        return str(e)

    return updated_data
