from unittest.mock import MagicMock

import src.DbHandler

import mongomock
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
    assert (db_handler.errorLog[0]["timestamp"] == str(datetime.datetime.now()))

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
        assert (db_handler.errorLog[0]["timestamp"] == str(datetime.datetime.now()))
    else:
        print ("Doc found"+str(docs.count()))
        assert False