import pandas as pd
from pymongo import MongoClient
import urllib.parse


def connect_mongo(host, port, username, password, db):
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (urllib.parse.quote_plus(username), urllib.parse.quote_plus(password), host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)


    return conn[db]


def mongoDataset(path, db, collection, query={}, host='localhost', port=27017, username=None, password=None, no_id=True):
    '''
            Generate Dataset from Mongo local database
    '''

    db = connect_mongo(host=host, port=port, username=username, password=password, db=db)

    # Make a query to the specific DB and Collection
    print("FINDING TRADES TRADES ...")
    cursor = db[collection].find(query)
    # Expand the cursor and construct the DataFrame

    df =  pd.DataFrame(list(cursor))

    # Delete the _id
    if no_id:
        del df['_id']

    # Create Csv file
    print("GENERATING CSV FILE ...")
    df.to_csv(path + "/dataset.csv", index=False)
    print("CSV FILE OK")
    print("Check",path + "/dataset.csv")