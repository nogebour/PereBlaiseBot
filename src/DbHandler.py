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
        self.connection_url = "mongodb+srv://"+os.environ['MONGO_DB_USER']+":"+os.environ['MONGO_DB_PASSWORD']+"@"+os.environ['MONGO_DB_INSTANCE']+"/"
        clientMongo = pymongo.MongoClient(self.connection_url)
        try:
            for doc in clientMongo.pereBlaise.games.find({self.key_name:self.party_name}):
                self.data = doc
        except ValueError:
            print("Error")
            clientMongo.close()
            return
        clientMongo.close()

    def updateGame(self):
        clientMongo = pymongo.MongoClient(self.connection_url)
        try:
            find_one_and_replace(clientMongo, self.key_name, self.party_name, self.data)
        except ValueError:
            print("Error")
        clientMongo.close()
        print(self.data)

    def saveSnapshotGame(self, removeCurrentImage = False):
        self.data[self.key_name] = self.snapshot_name+self.key_game+datetime.datetime.now().strftime(self.snapshotPattern)
        clientMongo = pymongo.MongoClient(self.connection_url)
        try:
            if removeCurrentImage:
                find_one_and_replace(clientMongo, self.key_name, self.party_name, self.data)
            else:
                self.data.pop('_id')
                insert(clientMongo, self.data)
        except ValueError:
            print("Error")
        clientMongo.close()
        print(self.data)


def insert(clientMongo, data):
    clientMongo.pereBlaise.games.insert(data)

def find_one_and_replace(clientMongo, key_name, party_name, data):
    clientMongo.pereBlaise.games.find_one_and_replace({key_name: party_name}, data)
