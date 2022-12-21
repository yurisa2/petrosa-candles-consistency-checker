import pymongo
import os
import datetime

client_mg = pymongo.MongoClient(
                                os.getenv(
                                    'MONGO_URI', 'mongodb://root:wUx3uQRBC8@localhost:27017'),
                                readPreference='secondaryPreferred',
                                appname='petrosa-nosql-crypto'
                                )


col = client_mg.petrosa_crypto['backfill']

found = col.find_one({"state": 1,
                     "checked": False
                      }
                     )

if(found['period'] == '5m'):
    col_name = 'm5'
    count_check = 288
if(found['period'] == '15m'):
    col_name = 'm15'
    count_check = 96
if(found['period'] == '30m'):
    col_name = 'm30'
    count_check = 48
if(found['period'] == '1h'):
    col_name = 'h1'
    count_check = 24


check_col = 'candles_' + col_name

day_start = datetime.datetime.fromisoformat(found['day'])
day_end = day_start + datetime.timedelta(days=1)

candles_col = client_mg.petrosa_crypto[check_col]
candles_found = candles_col.find({"ticker": found['symbol'],
                                  "datetime": {"$gte": day_start, "$lt": day_end}})

candles_found = list(candles_found)
if(count_check == len(candles_found)):
    logging.warning(found, ' OK')
    col.update_one({"_id": found['_id']}, {"$set": {"checked": True}})
else:
    col.update_one({"_id": found['_id']}, {"$set": {"state": 0}})
