import src.PereBlaiseBot
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


def test_get_user_value():
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


def test_get_value():
    bot = src.PereBlaiseBot.PereBlaiseBot()

    assert bot.get_value_str("pb test 12") == "12"

    try:
        bot.get_value_str("pb toto")
        assert False
    except IndexError:
        assert True
    except Exception:
        assert False
