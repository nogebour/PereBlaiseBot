import pymongo
import datetime
import os

from .Error.ErrorManager import ErrorManager, ErrorCode



class DbHandler:
    snapshot_pattern = "%Y%m%d_%H%M"
    snapshot_name = "snapshot"
    key_game = "kornettoh"
    key_name = 'name'

    def __init__(self, party_name=key_game):
        self.party_name = party_name
        self.data = None
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
            ErrorManager().add_error(ErrorCode.NO_DOCUMENT_FOUND, "retrieve_game")
            client_mongo_db.close()
            return

        client_mongo_db.close()

    def update_game(self):
        client_mongo_db = self.create_mongo_db_client()
        result = True
        try:
            replace_result = self.replace_one(client_mongo_db)
            if replace_result.matched_count > 0:
                print("Id updated " + str(replace_result.upserted_id))
            else:
                raise ValueError()
        except ValueError:
            ErrorManager().add_error(ErrorCode.NO_DOCUMENT_FOUND, "update_game")
            result = False

        client_mongo_db.close()
        print(self.data)
        return result

    def save_snapshot_game(self):
        self.data[self.key_name] = self.snapshot_name +\
                                   self.key_game +\
                                   datetime.datetime.now().strftime(self.snapshot_pattern)
        client_mongo = self.create_mongo_db_client()
        inserted_id = None
        try:
            print(self.data)
            if "_id" in self.data:
                self.data.pop("_id")
            insert_result = self.insert_one(client_mongo)
            if insert_result is None or insert_result.inserted_id is None:
                raise ValueError()
            else:
                inserted_id = insert_result.inserted_id
        except ValueError:
            ErrorManager().add_error(ErrorCode.NO_DOCUMENT_INSERTED, "save_snapshot")

        client_mongo.close()
        return inserted_id

    def create_mongo_db_client(self):
        return pymongo.MongoClient(self.connection_url)  # pragma: no cover
        # We do not cover this line as we do not really want real connection to Database

    def insert_one(self, client_mongo_db):
        return client_mongo_db.pereBlaise.games.insert_one(self.data)

    def replace_one(self, client_mongo_db):
        return client_mongo_db.pereBlaise.games.replace_one({self.key_name: self.party_name}, self.data)
