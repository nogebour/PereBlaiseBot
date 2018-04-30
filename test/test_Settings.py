import mongomock
from unittest.mock import MagicMock

import src.Settings

import datetime

def test_filldata_and_init_ok():
    db_handler = src.DbHandler.DbHandler()
    mongo_db_client_mock = mongomock.MongoClient()
    db_handler.create_mongo_db_client = MagicMock(return_value=mongo_db_client_mock)
    json = {"name": "kornettoh",
            "settings": {"start_time": "01/01/2018 - 01:01",
                         "current_time": "02/01/2018 - 02:02",
                         "players": ["John Doe",
                                     "Jane Doe",
                                     "Chuck Norris"]}}
    mongo_db_client_mock.pereBlaise.games.insert(json)
    setting = src.Settings.SettingsHandler()
    setting.dbHandler = db_handler
    setting.initialize()
    assert (json == setting.data)
    assert (setting.data["name"] == "kornettoh")
    assert (setting.start_time.strftime("%d/%m/%Y - %H:%M") == json["settings"]["start_time"])
    assert (setting.current_time.strftime("%d/%m/%Y - %H:%M") == json["settings"]["current_time"])
    assert (setting.players == json["settings"]["players"])
    assert (len(db_handler.errorLog) == 0)
    return setting, json["settings"]["start_time"], json["settings"]["current_time"]

def test_elpased_time():
    setting, start, current = test_filldata_and_init_ok()
    assert (setting.get_elapsed_time() ==
            (datetime.datetime.strptime(current, "%d/%m/%Y - %H:%M") -
             datetime.datetime.strptime(start, "%d/%m/%Y - %H:%M")))

def test_add_time_60_minutes():
    setting, start, current = test_filldata_and_init_ok()
    newTime = setting.add_time(60)
    assert (setting.current_time == newTime)
    assert (setting.current_time.strftime("%d/%m/%Y - %H:%M") == "02/01/2018 - 03:02")

def test_add_time_60000_minutes():
    setting, start, current = test_filldata_and_init_ok()
    newTime = setting.add_time(60000)
    assert (setting.current_time == newTime)
    assert (setting.current_time.strftime("%d/%m/%Y - %H:%M") == "12/02/2018 - 18:02")

def test_save_settings():
    setting, start, current = test_filldata_and_init_ok()
    setting.add_time(60)
    setting.save_settings()
    assert (setting.dbHandler.data['settings']['current_time'] == "02/01/2018 - 03:02")
