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
