import mongomock
from unittest.mock import MagicMock

import src.Settings
import src.DbHandler
import src.CharacterDBHandler

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
    setting.db_handler = db_handler
    setting.initialize()
    assert (json == setting.data)
    assert (setting.data["name"] == "kornettoh")
    assert (setting.start_time.strftime("%d/%m/%Y - %H:%M") == json["settings"]["start_time"])
    assert (setting.current_time.strftime("%d/%m/%Y - %H:%M") == json["settings"]["current_time"])
    assert (setting.players == json["settings"]["players"])
    assert (len(db_handler.error_log) == 0)
    return setting, json["settings"]["start_time"], json["settings"]["current_time"]


def test_elpased_time():
    setting, start, current = test_filldata_and_init_ok()
    assert (setting.get_elapsed_time() ==
            (datetime.datetime.strptime(current, "%d/%m/%Y - %H:%M") -
             datetime.datetime.strptime(start, "%d/%m/%Y - %H:%M")))


def test_add_time_60_minutes():
    setting, start, current = test_filldata_and_init_ok()
    new_time = setting.add_time(60)
    assert (setting.current_time == new_time)
    assert (setting.current_time.strftime("%d/%m/%Y - %H:%M") == "02/01/2018 - 03:02")


def test_add_time_60000_minutes():
    setting, start, current = test_filldata_and_init_ok()
    new_time = setting.add_time(60000)
    assert (setting.current_time == new_time)
    assert (setting.current_time.strftime("%d/%m/%Y - %H:%M") == "12/02/2018 - 18:02")


def test_save_settings():
    setting, start, current = test_filldata_and_init_ok()
    setting.add_time(60)
    setting.save_settings()
    assert (setting.db_handler.data['settings']['current_time'] == "02/01/2018 - 03:02")


def test_compute_rest_normal_too_long():
    setting = src.Settings.SettingsHandler()
    heal = setting.compute_rest("normal", 600)
    assert (heal == 2)


def test_compute_rest_normal():
    setting = src.Settings.SettingsHandler()
    heal = setting.compute_rest("normal", 300)
    assert (heal == 1)


def test_compute_rest_bon():
    setting = src.Settings.SettingsHandler()
    heal = setting.compute_rest("bon", 300)
    assert (heal == 2)


def test_compute_rest_excellent():
    setting = src.Settings.SettingsHandler()
    heal = setting.compute_rest("excellent", 300)
    assert (heal == 5)


def test_compute_rest_wrong_quality():
    setting = src.Settings.SettingsHandler()
    try:
        setting.compute_rest("excellentsasas", 300)
        assert False
    except ValueError:
        assert len(setting.error_log) == 1
        assert setting.error_log[0]["error_code"] == 3
        assert setting.error_log[0]["error_msg"] == "Invalid Rest Quality"
        assert setting.error_log[0]["context"] == "compute_rest"


def test_compute_walk_normal_too_long():
    setting = src.Settings.SettingsHandler()
    injury = setting.compute_walk("normale", 600)
    assert (injury == 3)


def test_compute_walk_normal():
    setting = src.Settings.SettingsHandler()
    injury = setting.compute_walk("normale", 300)
    assert (injury == 0)


def test_compute_walk_fast():
    setting = src.Settings.SettingsHandler()
    injury = setting.compute_walk("rapide", 300)
    assert (injury == 2)


def test_compute_walk_fastest():
    setting = src.Settings.SettingsHandler()
    injury = setting.compute_walk("barbare", 300)
    assert (injury == 3)


def test_compute_walk_wrong_quality():
    setting = src.Settings.SettingsHandler()
    print(len(setting.error_log))
    try:
        setting.compute_walk("excellentsasas", 300)
        assert False
    except ValueError:
        print("Expected")

    assert len(setting.error_log) == 1
    assert setting.error_log[0]["error_code"] == 4
    assert setting.error_log[0]["error_msg"] == "Invalid Walk Quality"
    assert setting.error_log[0]["context"] == "compute_walk"
