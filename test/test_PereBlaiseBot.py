from unittest.mock import MagicMock

import random
import src.PereBlaiseBot
import src.Settings
import src.Error.ErrorManager
import discord


def test_check_args():
    bot = src.PereBlaiseBot.PereBlaiseBot()
    help_msg = "error Message"

    embed = bot.check_args("test 1 2 3", 4, help_msg)
    if embed is None:
        assert True
    else:
        assert False

    embed = bot.check_args("test 1 2 3 4", 4, help_msg)
    if embed is None:
        assert True
    else:
        assert False

    embed = bot.check_args("test 1 23", 4, help_msg)
    if embed is None:
        assert False
    else:
        assert len(embed.fields) == 1
        assert embed.fields[0].value == help_msg
        assert embed.fields[0].name == "Erreur"


def test_extract_id():
    bot = src.PereBlaiseBot.PereBlaiseBot()

    assert bot.extract_id("<@!123456789>") == "123456789"
    assert bot.extract_id("<@123456789>") == "123456789"
    assert bot.extract_id("<!123456789>") is None
    assert bot.extract_id("<@!123456789sdffgfg") == "123456789sdffgf"


def test_get_user():
    bot = src.PereBlaiseBot.PereBlaiseBot()
    message = discord.Message(reactions=[])
    message.author.id = "987654321"

    assert bot.get_user(["toto", "<@!123456789>"], message, 1) == "123456789"
    assert bot.get_user(["toto", "<@!123456789>"], message, 0) == "987654321"
    assert bot.get_user(["toto", "<@!123456789>"], message, 2) == "987654321"


def test_get_user_value():
    bot = src.PereBlaiseBot.PereBlaiseBot()
    message = discord.Message(reactions=[])
    message.author.id = "987654321"

    assert bot.get_user_value("pb test <@!123456789> 12") == ("123456789", 12)
    try:
        bot.get_user_value("pb test <@!123456789> toto")
        assert False
    except ValueError:
        assert True
    except Exception:
        assert False

    try:
        bot.get_user_value("pb <@!123456789> toto")
        assert False
    except IndexError:
        assert True
    except Exception:
        assert False


def test_get_value():
    bot = src.PereBlaiseBot.PereBlaiseBot()

    assert bot.get_value("pb test 12") == 12
    try:
        bot.get_value("pb test toto")
        assert False
    except ValueError:
        assert True
    except Exception:
        assert False

    try:
        bot.get_value("pb toto")
        assert False
    except IndexError:
        assert True
    except Exception:
        assert False


def test_get_user_value_str():
    bot = src.PereBlaiseBot.PereBlaiseBot()
    message = discord.Message(reactions=[])
    message.author.id = "987654321"

    assert bot.get_user_value_str("pb test <@!123456789> 12") == ("123456789", "12")

    try:
        bot.get_user_value_str("pb <@!123456789> toto")
        assert False
    except IndexError:
        assert True
    except Exception:
        assert False


def test_get_value_str():
    bot = src.PereBlaiseBot.PereBlaiseBot()

    assert bot.get_value_str("pb test 12") == "12"

    try:
        bot.get_value_str("pb toto")
        assert False
    except IndexError:
        assert True
    except Exception:
        assert False


def test_make_time_operation_not_gm():
    src.Error.ErrorManager.ErrorManager().clear_error()
    message = discord.Message(reactions=[])
    message.author.id = "294164488427405313"
    json = {"name": "kornettoh",
            "settings": {"start_time": "01/01/2018 - 01:01",
                         "current_time": "02/01/2018 - 02:02",
                         "players": ["John Doe",
                                     "Jane Doe",
                                     "Chuck Norris"],
                         'characters': [{'PLAYER': "123456789"},
                                        {'PLAYER': "987654321"}]}}

    bot = src.PereBlaiseBot.PereBlaiseBot()
    settings = src.Settings.SettingsHandler()
    settings.db_handler.data = json

    embed = discord.Embed()

    assert not bot.make_time_operation("10", message, settings, embed)
    assert len(src.Error.ErrorManager.ErrorManager.error_log) == 1
    assert src.Error.ErrorManager.ErrorManager.error_log[0].error_type ==\
        src.Error.ErrorManager.ErrorCode.GM_COMMAND_ONLY

def test_make_time_operation_mj():
    message = discord.Message(reactions=[])
    message.author.id = "294164488427405312"
    json = {"name": "kornettoh",
            "settings": {"start_time": "01/01/2018 - 01:01",
                         "current_time": "02/01/2018 - 02:02",
                         "players": ["John Doe",
                                     "Jane Doe",
                                     "Chuck Norris"],
                         'characters': [{'PLAYER': "123456789"},
                                        {'PLAYER': "987654321"}]}}

    bot = src.PereBlaiseBot.PereBlaiseBot()
    settings = src.Settings.SettingsHandler()
    settings.data = json
    settings.fill_data()

    embed = discord.Embed()

    assert bot.make_time_operation("10", message, settings, embed)
    assert embed.fields[0].value == "<@294164488427405312> a demandé l'ajout de 10 minutes.\n" \
                                    "Nous sommes donc maintenant le 02/01/2018 à 02:12."


def test_make_time_operation_not_an_integer():
    src.Error.ErrorManager.ErrorManager().clear_error()
    message = discord.Message(reactions=[])
    message.author.id = "294164488427405312"
    json = {"name": "kornettoh",
            "settings": {"start_time": "01/01/2018 - 01:01",
                         "current_time": "02/01/2018 - 02:02",
                         "players": ["John Doe",
                                     "Jane Doe",
                                     "Chuck Norris"],
                         'characters': [{'PLAYER': "123456789"},
                                        {'PLAYER': "987654321"}]}}

    bot = src.PereBlaiseBot.PereBlaiseBot()
    settings = src.Settings.SettingsHandler()
    settings.data = json
    settings.fill_data()

    embed = discord.Embed()

    assert not bot.make_time_operation("toto", message, settings, embed)
    assert src.Error.ErrorManager.ErrorManager.error_log[0].error_type ==\
        src.Error.ErrorManager.ErrorCode.NOT_AN_INTEGER


def test_make_time_operation_negative():
    src.Error.ErrorManager.ErrorManager().clear_error()
    message = discord.Message(reactions=[])
    message.author.id = "294164488427405312"
    json = {"name": "kornettoh",
            "settings": {"start_time": "01/01/2018 - 01:01",
                         "current_time": "02/01/2018 - 02:02",
                         "players": ["John Doe",
                                     "Jane Doe",
                                     "Chuck Norris"],
                         'characters': [{'PLAYER': "123456789"},
                                        {'PLAYER': "987654321"}]}}

    bot = src.PereBlaiseBot.PereBlaiseBot()
    settings = src.Settings.SettingsHandler()
    settings.data = json
    settings.fill_data()

    embed = discord.Embed()

    assert not bot.make_time_operation("-10", message, settings, embed)
    assert src.Error.ErrorManager.ErrorManager.error_log[0].error_type ==\
        src.Error.ErrorManager.ErrorCode.NOT_A_POSITIVE_INTEGER


def test_apply_heal():
    bot = src.PereBlaiseBot.PereBlaiseBot()
    bot.character_db_handler.initialize = MagicMock()
    bot.character_db_handler.increase_ev = MagicMock(return_value="11")

    embed = discord.Embed()

    bot.apply_heal(embed, "123456789", "10")
    assert embed.fields[0].value == "Le joueur <@123456789> a soigné 10 points de vie.\nIl reste 11 points de vie."
    assert embed.fields[0].name == "Soin enregistré"


def test_apply_injury():
    bot = src.PereBlaiseBot.PereBlaiseBot()
    bot.character_db_handler.initialize = MagicMock()
    bot.character_db_handler.decrease_ev = MagicMock(return_value="11")

    embed = discord.Embed()

    bot.apply_injury(embed, "123456789", "10")
    assert embed.fields[0].value == "Le joueur <@123456789> a reçu 10 points de dégats.\nIl reste 11 points de vie."
    assert embed.fields[0].name == "Blessure enregistrée"


def throw_dices():
    bot = src.PereBlaiseBot.PereBlaiseBot()
    random.randint = MagicMock(return_value=1)

    result, str_display = bot.throw_dices("2D6", None, "")
    assert result == 2
    assert str_display == "1+1"
    assert len(src.Error.ErrorManager.ErrorManager.error_log) == 0


def throw_dices_with_existing_values():
    bot = src.PereBlaiseBot.PereBlaiseBot()
    random.randint = MagicMock(return_value=1)

    result, str_display = bot.throw_dices("2D6", 4, "1+1")
    assert result == 6
    assert str_display == "1+11+1"
    assert len(src.Error.ErrorManager.ErrorManager.error_log) == 0


def throw_dices_with_non_integer_dices():
    bot = src.PereBlaiseBot.PereBlaiseBot()
    random.randint = MagicMock(return_value=1)

    result, str_display = bot.throw_dices("2Dtoto", 4, "1+1")
    assert result is None
    assert str_display == ""
    assert src.Error.ErrorManager.ErrorManager.error_log[0].error_type ==\
        src.Error.ErrorManager.ErrorCode.NOT_AN_INTEGER


def throw_dices_with_negqtive_dices():
    bot = src.PereBlaiseBot.PereBlaiseBot()
    random.randint = MagicMock(return_value=1)

    result, str_display = bot.throw_dices("2D-2", 4, "1+1")
    assert result is None
    assert str_display == ""
    assert src.Error.ErrorManager.ErrorManager.error_log[0].error_type ==\
        src.Error.ErrorManager.ErrorCode.NOT_A_POSITIVE_INTEGER
