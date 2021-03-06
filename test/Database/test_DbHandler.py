
import src.CharacterDBHandler
import src.Database.DbHandler
import src.Error.ErrorManager


from unittest.mock import MagicMock
import datetime
import mongomock
import pymongo.results
import pymongo.errors


def mock_create_mongo_db_client():
    return mongomock.MongoClient()


def test_init():
    db_handler = src.Database.DbHandler.DbHandler()
    assert (db_handler.connection_url == "mongodb+srv://test1:test2@Test3/")


def test_wrong_url():
    src.Error.ErrorManager.ErrorManager().clear_error()
    db_handler = src.Database.DbHandler.DbHandler()
    try:
        db_handler.retrieve_game()
        assert False
    except pymongo.errors.ConfigurationError:
        assert len(src.Error.ErrorManager.ErrorManager.error_log) == 1
        error = src.Error.ErrorManager.ErrorManager.error_log[0]
        assert error.error_type == src.Error.ErrorManager.ErrorCode.UNABLE_TO_CONNECT_DB
        assert error.context == "create_mongo_db_client"
    except :
        assert False

def test_retrieve_game_ok():
    src.Error.ErrorManager.ErrorManager().clear_error()
    db_handler = src.Database.DbHandler.DbHandler()
    mongo_db_client_mock = mongomock.MongoClient()
    db_handler.create_mongo_db_client = MagicMock(return_value=mongo_db_client_mock)
    mongo_db_client_mock.pereBlaise.games.insert({"name": "kornettoh", "game": 1})
    db_handler.retrieve_game()
    assert (db_handler.data["name"] == "kornettoh")
    assert (db_handler.data["game"] == 1)
    assert (len(src.Error.ErrorManager.ErrorManager.error_log) == 0)


def test_retrieve_game_ko():
    src.Error.ErrorManager.ErrorManager().clear_error()
    db_handler = src.Database.DbHandler.DbHandler()
    mongo_db_client_mock = mongomock.MongoClient()
    db_handler.create_mongo_db_client = MagicMock(return_value=mongo_db_client_mock)
    db_handler.retrieve_game()

    assert (db_handler.data is None)

    error_mgr = src.Error.ErrorManager.ErrorManager()
    assert (len(error_mgr.error_log) == 1)
    assert (error_mgr.error_log[0].error_type == src.Error.ErrorManager.ErrorCode.NO_DOCUMENT_FOUND)
    assert (error_mgr.error_log[0].context == "retrieve_game")


def test_update_game_ok():
    src.Error.ErrorManager.ErrorManager().clear_error()

    # Setup
    db_handler = src.Database.DbHandler.DbHandler()
    mongo_db_client_mock = mongomock.MongoClient()
    db_handler.create_mongo_db_client = MagicMock(return_value=mongo_db_client_mock)
    mongo_db_client_mock.pereBlaise.games.insert({"name": "kornettoh", "game": 1})
    new_json = {"name": "kornettoh", "game": 2}
    db_handler.data = new_json

    # Operation to test
    db_handler.update_game()

    # Assert
    docs = mongo_db_client_mock.pereBlaise.games.find({"name": "kornettoh"})
    if docs.count() is not 1:
        assert False
    else:
        assert (docs[0]["game"] == 2)
        assert (docs[0]["name"] == "kornettoh")
        assert (len(src.Error.ErrorManager.ErrorManager.error_log) == 0)


def test_save_snapshot_game_ok_without_id():
    src.Error.ErrorManager.ErrorManager().clear_error()

    # Setup
    db_handler = src.Database.DbHandler.DbHandler()
    mongo_db_client_mock = mongomock.MongoClient()
    db_handler.create_mongo_db_client = MagicMock(return_value=mongo_db_client_mock)
    new_json = {"name": "kornettoh", "game": 1}
    db_handler.data = new_json

    # Operation to test
    inserted_id = db_handler.save_snapshot_game()

    # Assert
    docs = mongo_db_client_mock.pereBlaise.games.find({"_id": inserted_id})
    print(mongo_db_client_mock.pereBlaise.games)
    print (docs.count())
    if docs.count() is not 1:
        assert False
    else:
        assert (docs[0]["game"] == 1)
        assert (docs[0]["name"] == "snapshotkornettoh"+datetime.datetime.now().strftime("%Y%m%d_%H%M"))
        assert (len(src.Error.ErrorManager.ErrorManager.error_log) == 0)


def test_saveSnapshotGame_ok():
    src.Error.ErrorManager.ErrorManager().clear_error()

    # Setup
    db_handler = src.Database.DbHandler.DbHandler()
    mongo_db_client_mock = mongomock.MongoClient()
    db_handler.create_mongo_db_client = MagicMock(return_value=mongo_db_client_mock)
    new_json = {"name": "kornettoh", "game": 1, "_id": 123456789}
    db_handler.data = new_json

    # Operation to test
    inserted_id = db_handler.save_snapshot_game()

    # Assert
    docs = mongo_db_client_mock.pereBlaise.games.find({"_id": inserted_id})
    print(mongo_db_client_mock.pereBlaise.games)
    print(docs.count())
    if docs.count() is not 1:
        assert False
    else:
        assert (docs[0]["game"] == 1)
        assert (docs[0]["name"] == "snapshotkornettoh"+datetime.datetime.now().strftime("%Y%m%d_%H%M"))
        assert (len(src.Error.ErrorManager.ErrorManager.error_log) == 0)


def test_update_game_ko():
    src.Error.ErrorManager.ErrorManager().clear_error()

    # Setup
    db_handler = src.Database.DbHandler.DbHandler()
    mongo_db_client_mock = mongomock.MongoClient()
    db_handler.create_mongo_db_client = MagicMock(return_value=mongo_db_client_mock)
    new_json = {"name": "kornettoh", "game": 2}
    db_handler.data = new_json

    # Operation to test
    db_handler.update_game()

    # Assert
    docs = mongo_db_client_mock.pereBlaise.games.find({"name": "kornettoh"})
    if docs.count() == 0:
        assert (len(src.Error.ErrorManager.ErrorManager.error_log) == 1)
        error = src.Error.ErrorManager.ErrorManager.error_log[0]
        assert (error.error_type == src.Error.ErrorManager.ErrorCode.NO_DOCUMENT_FOUND)
        assert (error.context == "update_game")
    else:
        print("Doc found"+str(docs.count()))
        assert False


def test_save_snapshot_game_ko():
    src.Error.ErrorManager.ErrorManager().clear_error()

    # Setup
    db_handler = src.Database.DbHandler.DbHandler()
    mongo_db_client_mock = mongomock.MongoClient()
    db_handler.create_mongo_db_client = MagicMock(return_value=mongo_db_client_mock)
    new_json = {"name": "kornettoh", "game": 2}
    db_handler.data = new_json
    insert_one_result = pymongo.results.InsertOneResult(None, True)
    db_handler.insert_one = MagicMock(return_value=insert_one_result)


    # Operation to test
    inserted_id = db_handler.save_snapshot_game()

    # Assert
    if inserted_id is None:
        assert (len(src.Error.ErrorManager.ErrorManager.error_log) == 1)
        error = src.Error.ErrorManager.ErrorManager.error_log[0]
        assert (error.error_type == src.Error.ErrorManager.ErrorCode.NO_DOCUMENT_INSERTED)
        assert (error.context == "save_snapshot")
    else:
        print("Doc found"+str(inserted_id))
        assert False


def test_read_doc_for_character():
    src.Error.ErrorManager.ErrorManager().clear_error()
    db_handler = src.Database.DbHandler.DbHandler()
    mongo_db_client_mock = mongomock.MongoClient()
    db_handler.create_mongo_db_client = MagicMock(return_value=mongo_db_client_mock)
    json = {"name": "kornettoh",
            "settings": {"start_time": "01/01/2018 - 01:01",
                         "current_time": "02/01/2018 - 02:02",
                         "players": ["John Doe",
                                     "Jane Doe",
                                     "Chuck Norris"],
                         'characters': [{'PLAYER': "123456789"},
                                        {'PLAYER': "987654321"}]}}
    mongo_db_client_mock.pereBlaise.games.insert(json)

    player = db_handler.read_file_for_character("987654321")
    assert "987654321" == player["PLAYER"]


def test_read_doc_for_character_without_database():
    src.Error.ErrorManager.ErrorManager().clear_error()
    db_handler = src.Database.DbHandler.DbHandler()
    json = {"name": "kornettoh",
            "settings": {"start_time": "01/01/2018 - 01:01",
                         "current_time": "02/01/2018 - 02:02",
                         "players": ["John Doe",
                                     "Jane Doe",
                                     "Chuck Norris"],
                         'characters': [{'PLAYER': "123456789"},
                                        {'PLAYER': "987654321"}]}}
    db_handler.data = json

    player = db_handler.read_file_for_character("987654321")
    assert "987654321" == player["PLAYER"]


def test_read_doc_for_character_without_character():
    src.Error.ErrorManager.ErrorManager().clear_error()
    db_handler = src.Database.DbHandler.DbHandler()
    json = {"name": "kornettoh",
            "settings": {"start_time": "01/01/2018 - 01:01",
                         "current_time": "02/01/2018 - 02:02",
                         "players": ["John Doe",
                                     "Jane Doe",
                                     "Chuck Norris"],
                         'characters': [{'PLAYER': "123456789"}]}}
    db_handler.data = json

    player = db_handler.read_file_for_character("987654321")
    assert player is None
    assert len(src.Error.ErrorManager.ErrorManager.error_log) == 1
    error = src.Error.ErrorManager.ErrorManager.error_log[0]
    assert error.error_type == src.Error.ErrorManager.ErrorCode.NO_CHARACTER_FOUND
    assert error.context == "read_file_for_character"
