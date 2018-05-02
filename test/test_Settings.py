import mongomock
from unittest.mock import MagicMock

import src.Settings
import src.CharacterDBHandler
import src.Database.DbHandler
import src.CharacterDBHandler
import src.Error.ErrorManager

import discord
import datetime


def test_filldata_and_init_ok():
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
    setting = src.Settings.SettingsHandler()
    setting.db_handler = db_handler

    assert setting.data is None
    assert db_handler.data is None

    setting.initialize()

    assert (json == setting.data)
    assert (setting.data["name"] == "kornettoh")
    assert (setting.start_time.strftime("%d/%m/%Y - %H:%M") == json["settings"]["start_time"])
    assert (setting.current_time.strftime("%d/%m/%Y - %H:%M") == json["settings"]["current_time"])
    assert (setting.players == json["settings"]["players"])
    if len(src.Error.ErrorManager.ErrorManager.error_log) != 0:
        print(src.Error.ErrorManager.ErrorManager.error_log[0])
        assert False

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
        assert len(src.Error.ErrorManager.ErrorManager.error_log) == 1
        error = src.Error.ErrorManager.ErrorManager.error_log[0]
        assert error.error_type == src.Error.ErrorManager.ErrorCode.INVALID_REST_QUALITY
        assert error.context == "compute_rest"


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
    src.Error.ErrorManager.ErrorManager().clear_error()
    setting = src.Settings.SettingsHandler()
    try:
        setting.compute_walk("excellentsasas", 300)
        assert False
    except ValueError:
        print("Expected")

    assert len(src.Error.ErrorManager.ErrorManager.error_log) == 1
    error = src.Error.ErrorManager.ErrorManager.error_log[0]
    assert error.error_type == src.Error.ErrorManager.ErrorCode.INVALID_WALK_SPEED
    assert error.context == "compute_walk"


def test_handle_rest():
    setting = src.Settings.SettingsHandler()
    character_db_handler = src.CharacterDBHandler.CharacterDBHandler()
    character_db_handler.increase_ev_group = MagicMock(return_value=[{'id': 'Satan', 'remainingLife': '666'},
                                                                     {'id': 'Dieu', 'remainingLife': '999'},
                                                                     {'id': 'Chuck Norris', 'remainingLife': '9999999'}])
    setting.get_character_db_handler = MagicMock(return_value=character_db_handler)
    an_embed = discord.Embed(color=0x00ff00)
    result = setting.handle_rest("bon", 480, an_embed)
    assert result
    assert len(an_embed.fields) == 3
    assert an_embed.fields[0].name == "Soin enregistrée"
    assert an_embed.fields[0].value == "Le joueur <@Satan> a soigné 4 points de vie.\nIl reste 666 points de vie."
    assert an_embed.fields[1].name == "Soin enregistrée"
    assert an_embed.fields[1].value == "Le joueur <@Dieu> a soigné 4 points de vie.\nIl reste 999 points de vie."
    assert an_embed.fields[2].name == "Soin enregistrée"
    assert an_embed.fields[2].value == "Le joueur <@Chuck Norris> a soigné 4 points de vie.\nIl reste 9999999 " \
                                       "points de vie."


def test_handle_walk():
    setting = src.Settings.SettingsHandler()
    character_db_handler = src.CharacterDBHandler.CharacterDBHandler()
    character_db_handler.increase_ev_group = MagicMock(return_value=[{'id': 'Satan', 'remainingLife': '666'},
                                                                     {'id': 'Dieu', 'remainingLife': '999'},
                                                                     {'id': 'Chuck Norris', 'remainingLife': '9999999'}])
    setting.get_character_db_handler = MagicMock(return_value=character_db_handler)
    an_embed = discord.Embed(color=0x00ff00)
    result = setting.handle_walk("normale", 480, an_embed)
    assert result
    assert len(an_embed.fields) == 3
    assert an_embed.fields[0].name == "Blessure enregistrée"
    assert an_embed.fields[0].value == "Le joueur <@Satan> a pris 0 points de dégats.\nIl reste 666 points de vie."
    assert an_embed.fields[1].name == "Blessure enregistrée"
    assert an_embed.fields[1].value == "Le joueur <@Dieu> a pris 0 points de dégats.\nIl reste 999 points de vie."
    assert an_embed.fields[2].name == "Blessure enregistrée"
    assert an_embed.fields[2].value == "Le joueur <@Chuck Norris> a pris 0 points de dégats.\nIl reste 9999999 " \
                                       "points de vie."


def test_handle_rest_not_integer():
    src.Error.ErrorManager.ErrorManager().clear_error()
    setting = src.Settings.SettingsHandler()
    character_db_handler = src.CharacterDBHandler.CharacterDBHandler()
    setting.get_character_db_handler = MagicMock(return_value=character_db_handler)
    an_embed = discord.Embed(color=0x00ff00)
    result = setting.handle_rest("normale", "toto", an_embed)
    assert (not result)
    assert len(an_embed.fields) == 0
    assert len(src.Error.ErrorManager.ErrorManager.error_log) == 1
    error = src.Error.ErrorManager.ErrorManager.error_log[0]
    assert error.error_type == src.Error.ErrorManager.ErrorCode.NOT_AN_INTEGER
    assert error.context == "handle_rest"


def test_handle_walk_not_integer():
    src.Error.ErrorManager.ErrorManager().clear_error()
    setting = src.Settings.SettingsHandler()
    character_db_handler = src.CharacterDBHandler.CharacterDBHandler()
    setting.get_character_db_handler = MagicMock(return_value=character_db_handler)
    an_embed = discord.Embed(color=0x00ff00)
    result = setting.handle_walk("normale", "toto", an_embed)
    assert (not result)
    assert len(an_embed.fields) == 0
    assert len(src.Error.ErrorManager.ErrorManager.error_log) == 1
    error = src.Error.ErrorManager.ErrorManager.error_log[0]
    assert error.error_type == src.Error.ErrorManager.ErrorCode.NOT_AN_INTEGER
    assert error.context == "handle_walk"


def test_handle_rest_invalid_quality():
    src.Error.ErrorManager.ErrorManager().clear_error()
    setting = src.Settings.SettingsHandler()
    character_db_handler = src.CharacterDBHandler.CharacterDBHandler()
    setting.get_character_db_handler = MagicMock(return_value=character_db_handler)
    an_embed = discord.Embed(color=0x00ff00)
    result = setting.handle_rest("yooy", 300, an_embed)
    assert (not result)
    assert len(an_embed.fields) == 0
    assert len(src.Error.ErrorManager.ErrorManager.error_log) == 1
    error = src.Error.ErrorManager.ErrorManager.error_log[0]
    assert error.error_type == src.Error.ErrorManager.ErrorCode.INVALID_REST_QUALITY
    assert error.context == "compute_rest"


def test_handle_walk_invalid_speed():
    src.Error.ErrorManager.ErrorManager().clear_error()
    setting = src.Settings.SettingsHandler()
    character_db_handler = src.CharacterDBHandler.CharacterDBHandler()
    setting.get_character_db_handler = MagicMock(return_value=character_db_handler)
    an_embed = discord.Embed(color=0x00ff00)
    result = setting.handle_walk("yoyo", 300, an_embed)
    assert (not result)
    assert len(an_embed.fields) == 0
    assert len(src.Error.ErrorManager.ErrorManager.error_log) == 1
    error = src.Error.ErrorManager.ErrorManager.error_log[0]
    assert error.error_type == src.Error.ErrorManager.ErrorCode.INVALID_WALK_SPEED
    assert error.context == "compute_walk"

