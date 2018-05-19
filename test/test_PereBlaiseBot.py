from unittest.mock import MagicMock
from unittest.mock import Mock

import random
import src.PereBlaiseBot
import src.Settings
import src.Error.ErrorManager
import discord


def test_check_args():
    src.Error.ErrorManager.ErrorManager().clear_error()
    bot = src.PereBlaiseBot.PereBlaiseBot()
    help_msg = "error Message"

    bot.check_args("test 1 2 3", 4, help_msg)
    assert len(src.Error.ErrorManager.ErrorManager.error_log) == 0

    bot.check_args("test 1 2 3 4", 4, help_msg)
    assert len(src.Error.ErrorManager.ErrorManager.error_log) == 0

    bot.check_args("test 1 23", 4, help_msg)
    assert len(src.Error.ErrorManager.ErrorManager.error_log) == 1
    assert src.Error.ErrorManager.ErrorManager.error_log[0].error_type ==\
        src.Error.ErrorManager.ErrorCode.INVALID_SYNTAX


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

    assert bot.get_user_value("test <@!123456789> 12", 1, 2) == ("123456789", 12)


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


def test_throw_dices():
    src.Error.ErrorManager.ErrorManager().clear_error()
    bot = src.PereBlaiseBot.PereBlaiseBot()
    random.randint = MagicMock(return_value=1)

    result, str_display = bot.throw_dices("2", "6", None, "")
    assert result is None
    assert str_display == "1+1+"
    assert len(src.Error.ErrorManager.ErrorManager.error_log) == 0


def test_throw_dices_with_existing_values():
    src.Error.ErrorManager.ErrorManager().clear_error()
    bot = src.PereBlaiseBot.PereBlaiseBot()
    random.randint = MagicMock(return_value=1)

    result, str_display = bot.throw_dices("2", "6", 4, "1+1")
    assert result == 6
    assert str_display == "1+11+1+"
    assert len(src.Error.ErrorManager.ErrorManager.error_log) == 0


def test_throw_dices_with_non_integer_dices():
    src.Error.ErrorManager.ErrorManager().clear_error()
    bot = src.PereBlaiseBot.PereBlaiseBot()
    random.randint = MagicMock(return_value=1)

    result, str_display = bot.throw_dices("2", "toto", 4, "1+1")
    assert result is None
    assert str_display == ""
    assert src.Error.ErrorManager.ErrorManager.error_log[0].error_type ==\
        src.Error.ErrorManager.ErrorCode.NOT_AN_INTEGER


def test_throw_dices_with_negative_dices():
    src.Error.ErrorManager.ErrorManager().clear_error()
    bot = src.PereBlaiseBot.PereBlaiseBot()
    random.randint = MagicMock(return_value=1)

    result, str_display = bot.throw_dices("2", "-2", 4, "1+1")
    assert result is None
    assert str_display == ""
    assert src.Error.ErrorManager.ErrorManager.error_log[0].error_type ==\
        src.Error.ErrorManager.ErrorCode.NOT_A_POSITIVE_INTEGER


def test_throw_dices_with_negative_occ():
    src.Error.ErrorManager.ErrorManager().clear_error()
    bot = src.PereBlaiseBot.PereBlaiseBot()
    random.randint = MagicMock(return_value=1)

    result, str_display = bot.throw_dices("-2", "6", 4, "1+1")
    assert result is None
    assert str_display == ""
    assert src.Error.ErrorManager.ErrorManager.error_log[0].error_type ==\
        src.Error.ErrorManager.ErrorCode.NOT_A_POSITIVE_INTEGER


def test_compute_and_display_single_operation():
    src.Error.ErrorManager.ErrorManager().clear_error()
    bot = src.PereBlaiseBot.PereBlaiseBot()
    random.randint = MagicMock(return_value=1)

    result, str_display = bot.compute_and_display_single_operation("1d6", 4, "4+")
    assert result == 5
    assert str_display == "4+(1)"
    assert len(src.Error.ErrorManager.ErrorManager.error_log) == 0


def test_compute_and_display_single_operation_wrong_syntax():
    src.Error.ErrorManager.ErrorManager().clear_error()
    bot = src.PereBlaiseBot.PereBlaiseBot()
    random.randint = MagicMock(return_value=1)

    result, str_display = bot.compute_and_display_single_operation("1d6d6", 4, "4+")
    assert result is None
    assert str_display == ""
    assert len(src.Error.ErrorManager.ErrorManager.error_log) == 1
    assert src.Error.ErrorManager.ErrorManager.error_log[0].error_type ==\
        src.Error.ErrorManager.ErrorCode.INVALID_SYNTAX
    assert src.Error.ErrorManager.ErrorManager.error_log[0].error_args[0] == "[0-9]*[d,D][0-9]*"


def test_compute_and_display_single_operation_propagate_errors():
    src.Error.ErrorManager.ErrorManager().clear_error()
    bot = src.PereBlaiseBot.PereBlaiseBot()
    random.randint = MagicMock(return_value=1)

    result, str_display = bot.compute_and_display_single_operation("-2d6", 4, "4+")
    assert result is None
    assert str_display == ""
    assert src.Error.ErrorManager.ErrorManager.error_log[0].error_type ==\
        src.Error.ErrorManager.ErrorCode.NOT_A_POSITIVE_INTEGER


def test_compute_and_display_single_operation_int_op():
    src.Error.ErrorManager.ErrorManager().clear_error()
    bot = src.PereBlaiseBot.PereBlaiseBot()
    random.randint = MagicMock(return_value=1)

    result, str_display = bot.compute_and_display_single_operation("toto", 4, "4+")
    assert result is None
    assert str_display == ""
    assert len(src.Error.ErrorManager.ErrorManager.error_log) == 1
    assert src.Error.ErrorManager.ErrorManager.error_log[0].error_type ==\
        src.Error.ErrorManager.ErrorCode.NOT_AN_INTEGER


def test_display_result_status_success():
    bot = src.PereBlaiseBot.PereBlaiseBot()
    random.randint = MagicMock(return_value=1)

    str_display = bot.display_result_status(4, "4", 10)
    assert str_display == "4<10 --> Reussite"


def test_display_result_status_failure():
    bot = src.PereBlaiseBot.PereBlaiseBot()
    random.randint = MagicMock(return_value=1)

    str_display = bot.display_result_status(4, "4", 3)
    assert str_display == "4<3 --> Echec"


def test_display_result_status_none():
    bot = src.PereBlaiseBot.PereBlaiseBot()
    random.randint = MagicMock(return_value=1)

    str_display = bot.display_result_status(4, "4", None)
    assert str_display == "4"


def test_roll_ok():
    bot = src.PereBlaiseBot.PereBlaiseBot()
    random.randint = MagicMock(return_value=2)

    str_display = bot.roll("1d6 + 2d12 & 12 & 1D6 < 2 & 1D6 < 5")
    print(str_display)
    assert str_display == "1d6+2d12=(2)+(2+2)=6\n12=12=12\n1D6=(2)=2<2 --> Echec\n1D6=(2)=2<5 --> Reussite"


def test_represents_int():
    bot = src.PereBlaiseBot.PereBlaiseBot()
    assert bot.represents_int("12")
    assert bot.represents_int("-12")
    assert not bot.represents_int("toto")


def test_handle_insults():
    bot = src.PereBlaiseBot.PereBlaiseBot()
    result, gif = bot.handle_insults("blaise toto fuck")
    assert result
    assert len(gif) > 0
    result, gif = bot.handle_insults("blaise toto encule")
    assert result
    assert len(gif) > 0
    result, gif = bot.handle_insults("blaise toto salopard")
    assert result
    assert len(gif) > 0
    result, gif = bot.handle_insults("blaise toto connard")
    assert result
    assert len(gif) > 0
    result, gif = bot.handle_insults("blaise toto batard")
    assert result
    assert len(gif) > 0
    result, gif = bot.handle_insults("blaise toto ass hole")
    assert result
    assert len(gif) > 0

    result, gif = bot.handle_insults("blaise toto pisse")
    assert result
    assert len(gif) > 0

    result, gif = bot.handle_insults("blaise toto bite")
    assert result
    assert len(gif) > 0
    result, gif = bot.handle_insults("blaise toto dick")
    assert result
    assert len(gif) > 0

    result, gif = bot.handle_insults("blaise toto whore")
    assert result
    assert len(gif) > 0
    result, gif = bot.handle_insults("blaise toto pute")
    assert result
    assert len(gif) > 0

    result, gif = bot.handle_insults("blaise toto")
    assert not result
    assert len(gif) == 0


def test_detect_command_keyword():
    bot = src.PereBlaiseBot.PereBlaiseBot()
    assert bot.detect_command_keyword("pèreBlàise")
    assert bot.detect_command_keyword("pB")


def test_handle_life_operations_heal():
    bot = src.PereBlaiseBot.PereBlaiseBot()
    message = discord.Message(reactions=[])
    message.author.id = "987654321"
    message.channel = "123456789"
    returned_msg = []

    bot.apply_heal = MagicMock()

    bot.handle_life_operations(["2"], message, returned_msg)

    assert len(returned_msg) == 1
    bot.apply_heal.assert_called_once_with(returned_msg[0].embed_msg, "987654321", 2)


def test_handle_life_operations_injury():
    bot = src.PereBlaiseBot.PereBlaiseBot()
    message = discord.Message(reactions=[])
    message.author.id = "987654321"
    message.channel = "123456789"
    returned_msg = []

    bot.apply_injury = MagicMock()

    bot.handle_life_operations(["-2"], message, returned_msg)

    assert len(returned_msg) == 1
    bot.apply_injury.assert_called_once_with(returned_msg[0].embed_msg, "987654321", 2)


def test_handle_life_operations_not_integer():
    src.Error.ErrorManager.ErrorManager().clear_error()
    bot = src.PereBlaiseBot.PereBlaiseBot()
    message = discord.Message(reactions=[])
    message.author.id = "987654321"
    message.channel = "123456789"
    returned_msg = []

    bot.handle_life_operations(["toto"], message, returned_msg)

    assert len(returned_msg) == 0
    assert len(src.Error.ErrorManager.ErrorManager.error_log) == 0


def test_handle_welcome():
    bot = src.PereBlaiseBot.PereBlaiseBot()
    message = discord.Message(reactions=[])
    message.channel = "123456789"
    returned_msg = []

    bot.handle_welcome(["hi"], message, returned_msg)

    assert len(returned_msg) == 1
    assert len(src.Error.ErrorManager.ErrorManager.error_log) == 0


def test_handle_welcome_not_matched():
    bot = src.PereBlaiseBot.PereBlaiseBot()
    message = discord.Message(reactions=[])
    message.channel = "123456789"
    returned_msg = []

    bot.handle_welcome(["hikjjifgijd"], message, returned_msg)

    assert len(returned_msg) == 0
    assert len(src.Error.ErrorManager.ErrorManager.error_log) == 0


def test_display_error():
    error_mgr = src.Error.ErrorManager.ErrorManager()
    error_mgr.clear_error()
    bot = src.PereBlaiseBot.PereBlaiseBot()

    error_mgr.add_error()
    error_mgr.add_error(src.Error.ErrorManager.ErrorCode.INVALID_SYNTAX,
                        "Test display error",
                        ["pb test diaplays"])
    returned_msgs = [src.PereBlaiseBot.DiscordMessage("123456789", "test")]

    bot.display_error(returned_msgs, "123456789")
    assert len(returned_msgs) == 3


def test_display_error_with_empty_error_log():
    error_mgr = src.Error.ErrorManager.ErrorManager()
    error_mgr.clear_error()
    bot = src.PereBlaiseBot.PereBlaiseBot()

    returned_msgs = [src.PereBlaiseBot.DiscordMessage("123456789", "test")]

    bot.display_error(returned_msgs, "123456789")
    assert len(returned_msgs) == 1


def test_gm_injury():
    error_mgr = src.Error.ErrorManager.ErrorManager()
    error_mgr.clear_error()

    bot = src.PereBlaiseBot.PereBlaiseBot()
    bot.apply_injury = Mock()

    message = discord.Message(reactions=[])
    message.channel = "123456789"
    message.author.id = src.PereBlaiseBot.MJ_ID
    message.content = "pb MJblessure <@123456789> 2"

    returned_msgs = [src.PereBlaiseBot.DiscordMessage("1234567890", "test")]

    bot.handle_gm_injury(["MJblessure", "<@123456789>", "2"], message, returned_msgs)
    assert len(returned_msgs) == 2
    assert returned_msgs[1].discord_channel == "123456789"
    bot.apply_injury.call_args()


def test_gm_injury_not_gm():
    error_mgr = src.Error.ErrorManager.ErrorManager()
    error_mgr.clear_error()

    bot = src.PereBlaiseBot.PereBlaiseBot()

    message = discord.Message(reactions=[])
    message.channel = "123456789"
    message.author.id = "987654312"
    message.content = "pb MJblessure <@123456789> 2"

    returned_msgs = [src.PereBlaiseBot.DiscordMessage("1234567890", "test")]

    bot.handle_gm_injury(["MJblessure", "<@123456789>", "2"], message, returned_msgs)
    assert len(returned_msgs) == 2
    assert returned_msgs[0].discord_channel == "1234567890"
    assert returned_msgs[1].discord_channel == "123456789"
    assert returned_msgs[1].embed_msg.fields[0].value == str(src.Error.ErrorManager.ErrorManager.error_log[0])


def test_gm_injury_not_matched():
    error_mgr = src.Error.ErrorManager.ErrorManager()
    error_mgr.clear_error()

    bot = src.PereBlaiseBot.PereBlaiseBot()

    message = discord.Message(reactions=[])
    message.channel = "123456789"
    message.author.id = "987654312"
    message.content = "pb toto <@123456789> 2"

    returned_msgs = [src.PereBlaiseBot.DiscordMessage("1234567890", "test")]

    bot.handle_gm_injury(["toto", "<@123456789>", "2"], message, returned_msgs)
    assert len(returned_msgs) == 1
    assert returned_msgs[0].discord_channel == "1234567890"


def test_gm_heal():
    error_mgr = src.Error.ErrorManager.ErrorManager()
    error_mgr.clear_error()

    bot = src.PereBlaiseBot.PereBlaiseBot()
    bot.apply_heal = Mock()

    message = discord.Message(reactions=[])
    message.channel = "123456789"
    message.author.id = src.PereBlaiseBot.MJ_ID
    message.content = "pb MJsoins <@123456789> 2"

    returned_msgs = [src.PereBlaiseBot.DiscordMessage("1234567890", "test")]

    bot.handle_gm_heal(["MJsoin", "<@123456789>", "2"], message, returned_msgs)
    assert len(returned_msgs) == 2
    assert returned_msgs[1].discord_channel == "123456789"


def test_gm_heal_not_gm():
    error_mgr = src.Error.ErrorManager.ErrorManager()
    error_mgr.clear_error()

    bot = src.PereBlaiseBot.PereBlaiseBot()

    message = discord.Message(reactions=[])
    message.channel = "123456789"
    message.author.id = "987654312"
    message.content = "pb MJsoin <@123456789> 2"

    returned_msgs = [src.PereBlaiseBot.DiscordMessage("1234567890", "test")]

    bot.handle_gm_heal(["MJsoin", "<@123456789>", "2"], message, returned_msgs)
    assert len(returned_msgs) == 2
    assert returned_msgs[0].discord_channel == "1234567890"
    assert returned_msgs[1].discord_channel == "123456789"
    assert returned_msgs[1].embed_msg.fields[0].value == str(src.Error.ErrorManager.ErrorManager.error_log[0])


def test_gm_heal_not_matched():
    error_mgr = src.Error.ErrorManager.ErrorManager()
    error_mgr.clear_error()

    bot = src.PereBlaiseBot.PereBlaiseBot()

    message = discord.Message(reactions=[])
    message.channel = "123456789"
    message.author.id = "987654312"
    message.content = "pb toto <@123456789> 2"

    returned_msgs = [src.PereBlaiseBot.DiscordMessage("1234567890", "test")]

    bot.handle_gm_heal(["toto", "<@123456789>", "2"], message, returned_msgs)
    assert len(returned_msgs) == 1
    assert returned_msgs[0].discord_channel == "1234567890"
