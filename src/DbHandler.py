import pymongo
import datetime
import os


class DbHandler:
    data = None
    snapshot_pattern = "%Y%m%d_%H%M"
    snapshot_name = "snapshot"
    key_game = "kornettoh"
    key_name = 'name'
    party_name = None

    def __init__(self, party_name=key_game):
        self.party_name = party_name
        self.error_log = []
        self.connection_url = "mongodb+srv://"+os.environ['MONGO_DB_USER']+\
                              ":"+os.environ['MONGO_DB_PASSWORD']+\
                              "@"+os.environ['MONGO_DB_INSTANCE']+"/"

    def retrieve_game(self):
        client_mongo_db = self.create_mongo_db_client()
        try:
            docs = client_mongo_db.pereBlaise.games.find({self.key_name: self.party_name})
            if docs.count() is 1:
                self.data = docs[0]
            else:
                raise ValueError()
        except ValueError:
            print("Error %s - %s" % (str(1).zfill(4), "No Document Found"))
            self.error_log.append({"error_code": 1,
                                  "error_msg": "No Document Found",
                                  "context": "Retrieve Game",
                                  "timestamp": datetime.datetime.now()})
            client_mongo_db.close()
            return
        client_mongo_db.close()

    def update_game(self):
        client_mongo_db = self.create_mongo_db_client()
        try:
            replace_result = replace_one(client_mongo_db, self.key_name, self.party_name, self.data)
            if replace_result.matched_count > 0:
                print("Id updated " + str(replace_result.upserted_id))
            else:
                raise ValueError()
        except ValueError:
            print("Error %s - %s" % (str(1).zfill(4),"No Document Found"))
            self.error_log.append({"error_code": 1,
                                  "error_msg": "No Document Found",
                                  "context": "Update Game",
                                  "timestamp": datetime.datetime.now()})
        client_mongo_db.close()
        print(self.data)

    def save_snapshot_game(self):
        self.data[self.key_name] = self.snapshot_name +\
                                   self.key_game +\
                                   datetime.datetime.now().strftime(self.snapshot_pattern)
        client_mongo = self.create_mongo_db_client()
        inserted_id = None
        try:
            print (self.data)
            if "_id" in self.data:
                self.data.pop("_id")
            insert_result = insert_one(client_mongo, self.data)
            if insert_result is None or insert_result.inserted_id is None:
                raise ValueError()
            else:
                inserted_id = insert_result.inserted_id
        except ValueError:
            print("Error %s - %s" % (str(2).zfill(4), "No Document Inserted"))
            self.error_log.append({"error_code": 2,
                                  "error_msg": "No Document Inserted",
                                  "context": "Save snapshot",
                                  "timestamp": datetime.datetime.now()})
        client_mongo.close()
        return inserted_id

    def create_mongo_db_client(self):
        return pymongo.MongoClient(self.connection_url)  # pragma: no cover
        # We do not cover this line as we do not really want real connection to Database


def insert_one(client_mongo_db, data):
    return client_mongo_db.pereBlaise.games.insert_one(data)


def replace_one(client_mongo_db, key_name, party_name, data):
    return client_mongo_db.pereBlaise.games.replace_one({key_name: party_name}, data)
