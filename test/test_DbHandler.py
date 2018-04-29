from unittest.mock import MagicMock

import src.DbHandler
import src.CharacterDBHandler

import mongomock
import pymongo.results
import datetime
import os


def mock_create_mongo_db_client():
    return mongomock.MongoClient()


def test_init():
    os.environ['MONGO_DB_USER'] = "test1"
    os.environ['MONGO_DB_PASSWORD'] = "test2"
    os.environ['MONGO_DB_INSTANCE'] = "Test3"
    db_handler = src.DbHandler.DbHandler()
    assert (db_handler.connection_url == "mongodb+srv://test1:test2@Test3/")

def test_retrieveGame_ok():
    db_handler = src.DbHandler.DbHandler()
    mongo_db_client_mock = mongomock.MongoClient()
    db_handler.create_mongo_db_client = MagicMock(return_value=mongo_db_client_mock)
    mongo_db_client_mock.pereBlaise.games.insert({"name":"kornettoh","game":1})
    db_handler.retrieveGame()
    assert (db_handler.data["name"] == "kornettoh")
    assert (db_handler.data["game"] == 1)
    assert (len(db_handler.errorLog) == 0)


def test_retrieveGame_ko():
    db_handler = src.DbHandler.DbHandler()
    mongo_db_client_mock = mongomock.MongoClient()
    db_handler.create_mongo_db_client = MagicMock(return_value=mongo_db_client_mock)
    db_handler.retrieveGame()
    assert (db_handler.data is None)
    assert (len(db_handler.errorLog) == 1)
    assert (db_handler.errorLog[0]["error_code"] == 1)
    assert (db_handler.errorLog[0]["error_msg"] == "No Document Found")
    assert (db_handler.errorLog[0]["context"] == "Retrieve Game")
    assert (db_handler.errorLog[0]["timestamp"].strftime("%Y-%m-%d %H:%M:%S") ==
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def test_updateGame_ok():

    #Setup
    db_handler = src.DbHandler.DbHandler()
    mongo_db_client_mock = mongomock.MongoClient()
    db_handler.create_mongo_db_client = MagicMock(return_value=mongo_db_client_mock)
    mongo_db_client_mock.pereBlaise.games.insert({"name":"kornettoh","game":1})
    new_json = {"name":"kornettoh","game":2}
    db_handler.data = new_json

    #Operation to test
    db_handler.updateGame()

    #Assert
    docs = mongo_db_client_mock.pereBlaise.games.find({"name": "kornettoh"})
    if docs.count() is not 1:
        assert False
    else:
        assert (docs[0]["game"] == 2)
        assert (docs[0]["name"] == "kornettoh")
        assert (len(db_handler.errorLog) == 0)


def test_saveSnapshotGame_ok_without_id():

    #Setup
    db_handler = src.DbHandler.DbHandler()
    mongo_db_client_mock = mongomock.MongoClient()
    db_handler.create_mongo_db_client = MagicMock(return_value=mongo_db_client_mock)
    new_json = {"name": "kornettoh", "game": 1}
    db_handler.data = new_json

    #Operation to test
    inserted_id = db_handler.saveSnapshotGame()

    #Assert
    docs = mongo_db_client_mock.pereBlaise.games.find({"_id": inserted_id})
    print(mongo_db_client_mock.pereBlaise.games)
    print (docs.count())
    if docs.count() is not 1:
        assert False
    else:
        assert (docs[0]["game"] == 1)
        assert (docs[0]["name"] == "snapshotkornettoh"+datetime.datetime.now().strftime("%Y%m%d_%H%M"))
        assert (len(db_handler.errorLog) == 0)


def test_saveSnapshotGame_ok():

    #Setup
    db_handler = src.DbHandler.DbHandler()
    mongo_db_client_mock = mongomock.MongoClient()
    db_handler.create_mongo_db_client = MagicMock(return_value=mongo_db_client_mock)
    new_json = {"name": "kornettoh", "game": 1, "_id": 123456789}
    db_handler.data = new_json

    #Operation to test
    inserted_id = db_handler.saveSnapshotGame()

    #Assert
    docs = mongo_db_client_mock.pereBlaise.games.find({"_id": inserted_id})
    print(mongo_db_client_mock.pereBlaise.games)
    print (docs.count())
    if docs.count() is not 1:
        assert False
    else:
        assert (docs[0]["game"] == 1)
        assert (docs[0]["name"] == "snapshotkornettoh"+datetime.datetime.now().strftime("%Y%m%d_%H%M"))
        assert (len(db_handler.errorLog) == 0)


def test_updateGame_ko():
    #Setup
    db_handler = src.DbHandler.DbHandler()
    mongo_db_client_mock = mongomock.MongoClient()
    db_handler.create_mongo_db_client = MagicMock(return_value=mongo_db_client_mock)
    new_json = {"name":"kornettoh","game":2}
    db_handler.data = new_json

    #Operation to test
    db_handler.updateGame()

    #Assert
    docs = mongo_db_client_mock.pereBlaise.games.find({"name": "kornettoh"})
    if (docs.count() == 0):
        assert (len(db_handler.errorLog) == 1)
        assert (db_handler.errorLog[0]["error_code"] == 1)
        assert (db_handler.errorLog[0]["error_msg"] == "No Document Found")
        assert (db_handler.errorLog[0]["context"] == "Update Game")
        assert (db_handler.errorLog[0]["timestamp"].strftime("%Y-%m-%d %H:%M:%S") ==
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    else:
        print ("Doc found"+str(docs.count()))
        assert False

def test_saveSnapshotGame_ko():
    #Setup
    db_handler = src.DbHandler.DbHandler()
    mongo_db_client_mock = mongomock.MongoClient()
    db_handler.create_mongo_db_client = MagicMock(return_value=mongo_db_client_mock)
    new_json = {"name":"kornettoh","game":2}
    db_handler.data = new_json
    insert_one_result = pymongo.results.InsertOneResult(None, True)
    src.DbHandler.insert_one = MagicMock(return_value=insert_one_result)


    #Operation to test
    inserted_id = db_handler.saveSnapshotGame()

    #Assert
    if inserted_id is None:
        assert (len(db_handler.errorLog) == 1)
        assert (db_handler.errorLog[0]["error_code"] == 2)
        assert (db_handler.errorLog[0]["error_msg"] == "No Document Inserted")
        assert (db_handler.errorLog[0]["context"] == "Save snapshot")
        assert (db_handler.errorLog[0]["timestamp"].strftime("%Y-%m-%d %H:%M:%S") ==
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    else:
        print ("Doc found"+inserted_id)
        assert False