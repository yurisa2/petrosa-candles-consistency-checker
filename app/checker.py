import pymongo
import os
import datetime
import time


class PETROSAdbchecker(object):
    def __init__(self):
        self.client_mg = pymongo.MongoClient(
                                        os.getenv(
                                            'MONGO_URI', 'mongodb://root:QnjfRW7nl6@localhost:27017'),
                                        readPreference='secondaryPreferred',
                                        appname='petrosa-apps-consistency-checker'
                                        )
        self.backfill_col = self.client_mg.petrosa_crypto['backfill']

    def check_db(self):
        try:
            found = self.backfill_col.find_one({"state": 1,
                                                "checked": False
                                                }
                                               )

            if not found:
                # print('Not suitable check to find')
                time.sleep(1)
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
                # print(found, ' OK')
                self.backfill_col.update_one({"_id": found['_id']}, {
                               "$set": {"checked": True}})
                return True

            else:
                print("hmmm thats wrong: ")
                print(found)

                if('checking_times' in found and found['checking_times'] > 5):
                    print('Exhausted tentatives for ', found)
                    self.backfill_col.update_one(
                        {"_id": found['_id']},
                        {"$set": {"state": 1, "checked": True}})

                elif('checking_times' in found and found['checking_times'] > 5):
                    found['checking_times'] += 1
                    self.backfill_col.update_one(
                        {"_id": found['_id']},
                        {"$set":
                         {"state": 0,
                          "checked": False,
                          "checking_times": found['checking_times']
                          }
                         })

                elif('checking_times' not in found):
                    self.backfill_col.update_one(
                        {"_id": found['_id']},
                        {"$set":
                         {"state": 0,
                          "checked": False,
                          "checking_times": 1
                          }
                         })

                return False

        except Exception as e:
            print('Error in checker', e)
            raise

    def run(self):
        while True:
            self.check_db()
