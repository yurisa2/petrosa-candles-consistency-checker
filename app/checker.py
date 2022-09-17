import pymongo
import os
import datetime


class PETROSAdbchecker(object):
    def __init__(self):
        self.client_mg = pymongo.MongoClient(
                                        os.getenv(
                                            'MONGO_URI', 'mongodb://root:wUx3uQRBC8@localhost:27017'),
                                        readPreference='secondaryPreferred',
                                        appname='petrosa-nosql-crypto'
                                        )
        self.backfill_col = self.client_mg.petrosa_crypto['backfill']

    def check_db(self):
        try:
            found = self.backfill_col.find_one({"state": 1,
                                                "checked": False
                                                }
                                               )

            if not found:
                return True

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

            candles_col = self.client_mg.petrosa_crypto[check_col]
            candles_found = candles_col.find({"ticker": found['symbol'],
                                              "datetime": {"$gte": day_start, "$lt": day_end}})

            candles_found = list(candles_found)
            if(count_check == len(candles_found)):
                print(found, ' OK')
                self.backfill_col.update_one({"_id": found['_id']}, {
                               "$set": {"checked": True}})
                return True
            else:
                self.backfill_col.update_one(
                    {"_id": found['_id']}, {"$set": {"state": 0}})
                return False

        except Exception as e:
            print('Error in checker', e)
            raise

    def run(self):
        while True:
            self.check_db()
