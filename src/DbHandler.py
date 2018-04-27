import pymongo
import datetime
import os

class DbHandler:
    data = None
    snapshotPattern = "%Y%m%d_%H%M"
    snapshot_name = "snapshot"
    key_game = "kornettoh"
    key_name = 'name'
    party_name = None

    def __init__(self, partyName = key_game):
        self.party_name = partyName
        self.errorLog = []
        self.connection_url = "mongodb+srv://"+os.environ['MONGO_DB_USER']+":"+os.environ['MONGO_DB_PASSWORD']+"@"+os.environ['MONGO_DB_INSTANCE']+"/"

    def retrieveGame(self):
        clientMongo = self.create_mongo_db_client()
        try:
            docs = clientMongo.pereBlaise.games.find({self.key_name: self.party_name})
            if docs.count() is 1:
                self.data = docs[0]
            else:
                raise ValueError()
        except ValueError:
            print("Error %s - %s" % (str(1).zfill(4),"No Document Found"))
            self.errorLog.append({"error_code":1,
                                  "error_msg":"No Document Found",
                                  "context":"Retrieve Game",
                                  "timestamp":datetime.datetime.now()})
            clientMongo.close()
            return
        clientMongo.close()

    def updateGame(self):
        clientMongo = self.create_mongo_db_client()
        try:
            replace_result = replace_one(clientMongo, self.key_name, self.party_name, self.data)
            if replace_result.matched_count > 0:
                print("Id updated " + str(replace_result.upserted_id))
            else:
                raise ValueError()
        except ValueError:
            print("Error %s - %s" % (str(1).zfill(4),"No Document Found"))
            self.errorLog.append({"error_code":1,
                                  "error_msg":"No Document Found",
                                  "context":"Update Game",
                                  "timestamp":datetime.datetime.now()})
        clientMongo.close()
        print(self.data)

    def saveSnapshotGame(self, removeCurrentImage = False):
        self.data[self.key_name] = self.snapshot_name+self.key_game+datetime.datetime.now().strftime(self.snapshotPattern)
        clientMongo = self.create_mongo_db_client()
        try:
            if removeCurrentImage:
                replace_one(clientMongo, self.key_name, self.party_name, self.data)
            else:
                self.data.pop('_id')
                insert(clientMongo, self.data)
        except ValueError:
            print("Error")
        clientMongo.close()
        print(self.data)

    def closeMongoDbClient(self, mongo_db_client):
        mongo_db_client.close()

    def create_mongo_db_client(self):
        return pymongo.MongoClient(self.connection_url)

def insert(clientMongo, data):
    clientMongo.pereBlaise.games.insert(data)

def replace_one(clientMongo, key_name, party_name, data):
    return clientMongo.pereBlaise.games.replace_one({key_name: party_name}, data)
