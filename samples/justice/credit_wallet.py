from justice import Justice


def credit_wallet(event, context):
    namespace = 'accelbyte'
    endpoint = "https://demo.accelbyte.io"
    core = Justice(namespace, endpoint)
    user_data = event['data']
    r = core.wallet.credit(user_data['userId'], 100, 'USD')
    print(r.json())
    return event['data']
