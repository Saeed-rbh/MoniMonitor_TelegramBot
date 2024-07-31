from datetime import datetime

def get_transactions(user_id, record_type):
    client = MongoClient('localhost', 27017)
    db = client['MoneyMonitor']
    collection_name = 'Daily' if record_type == 'daily' else 'Monthly'
    collection = db[user_id][collection_name]

    today = datetime.now()
    query = {
        'Year': today.year,
        'Month': today.month
    }

    records = list(collection.find(query))
    client.close()
    return records
