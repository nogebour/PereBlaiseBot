import src.CharacterDBHandler
import src.Database.DbHandler
import src.Error.ErrorManager
import discord.colour

from unittest.mock import MagicMock
import mongomock

def test_initialize_ok():
    src.Error.ErrorManager.ErrorManager().clear_error()
    db_handler = src.Database.DbHandler.DbHandler()
    mongo_db_client_mock = mongomock.MongoClient()
    db_handler.create_mongo_db_client = MagicMock(return_value=mongo_db_client_mock)
    mongo_db_client_mock.pereBlaise.games.insert({"name": "kornettoh", "game": 1})

    character_handler = src.CharacterDBHandler.CharacterDBHandler()
    character_handler.db_handler = db_handler
    character_handler.initialize()

    assert (character_handler.data["name"] == "kornettoh")
    assert (character_handler.data["game"] == 1)
    assert (len(src.Error.ErrorManager.ErrorManager.error_log) == 0)


def test_import_character():
    db_handler = src.Database.DbHandler.DbHandler()
    db_handler.data = {"name": "kornettoh",
                       "settings": {"characters": [{"PLAYER": "123456789",
                                                    "NAME": "Chuck Norris",
                                                    "RACE": "God",
                                                    "JOB": "Soldier",
                                                    "EV": 12,
                                                    "EVMAX": 25,
                                                    "EA": 13,
                                                    "EAMAX": 26,
                                                    "COU": 12,
                                                    "INT": 13,
                                                    "CHA": 25,
                                                    "AD": 17,
                                                    "FO": 18,
                                                    "AT": 14,
                                                    "PRD": 19,
                                                    "DESTINY": 2,
                                                    "SKILLS": ["Ultra strengh", "Iron Fist"],
                                                    "GOLD": 152,
                                                    "SILVER": 23,
                                                    "BRONZE": 14,
                                                    "LEVEL": 2,
                                                    "SEX": "Homme",
                                                    "XP": 423,
                                                    "STUFF": ["Rope", "Potion"],
                                                    "WEAPONS": ["Left fist", "Right fist"]}]}}

    character_handler = src.CharacterDBHandler.CharacterDBHandler()
    character_handler.db_handler = db_handler

    character = character_handler.import_character("123456789")

    assert character.adresse == 17
    assert character.attaque == 14
    assert character.charisme == 25
    assert character.competences == ["Ultra strengh", "Iron Fist"]
    assert character.courage == 12
    assert character.ea == 13
    assert character.ea_max == 26
    assert character.ev == 12
    assert character.ev_max == 25
    assert character.experience == 423
    assert character.force == 18
    assert character.intelligence == 13
    assert character.job == "Soldier"
    assert character.name == "Chuck Norris"
    assert character.niveau == 2
    assert character.parade == 19
    assert character.piecesArgent == 23
    assert character.piecesBronze == 14
    assert character.piecesOr == 152
    assert character.pointsDeDestin == 2
    assert character.sexe == "Homme"
    assert character.stuff == ["Rope", "Potion"]
    assert character.userName == "123456789"
    assert character.weapons == ["Left fist", "Right fist"]
    assert (len(src.Error.ErrorManager.ErrorManager.error_log) == 0)


def test_mapping_stat():
    character_handler = src.CharacterDBHandler.CharacterDBHandler()
    assert character_handler.convert_key(character_handler.key[0]) == "Race"
    assert character_handler.convert_key(character_handler.key[1]) == "Métier"
    assert character_handler.convert_key(character_handler.key[2]) == "Energie vitale"
    assert character_handler.convert_key(character_handler.key[3]) == "Energie vitale maximale"
    assert character_handler.convert_key(character_handler.key[4]) == "Energie astrale"
    assert character_handler.convert_key(character_handler.key[5]) == "Energie astrale maximale"
    assert character_handler.convert_key(character_handler.key[6]) == "Courage"
    assert character_handler.convert_key(character_handler.key[7]) == "Intelligence"
    assert character_handler.convert_key(character_handler.key[8]) == "Charisme"
    assert character_handler.convert_key(character_handler.key[9]) == "Adresse"
    assert character_handler.convert_key(character_handler.key[10]) == "Force"
    assert character_handler.convert_key(character_handler.key[11]) == "Attaque"
    assert character_handler.convert_key(character_handler.key[12]) == "Parade"
    assert character_handler.convert_key(character_handler.key[13]) == "Points de destin"
    assert character_handler.convert_key(character_handler.key[14]) == "Compétences"
    assert character_handler.convert_key(character_handler.key[15]) == "Pièces d'or"
    assert character_handler.convert_key(character_handler.key[16]) == "Pièces d'argent"
    assert character_handler.convert_key(character_handler.key[17]) == "Pièces de bronze"
    assert character_handler.convert_key(character_handler.key[18]) == "Niveau"
    assert character_handler.convert_key(character_handler.key[19]) == "Sexe"
    assert character_handler.convert_key(character_handler.key[20]) == "Points d'expérience"
    assert character_handler.convert_key(character_handler.key[21]) == "Nom"
    assert character_handler.convert_key(character_handler.key[22]) == "Equipement"
    assert character_handler.convert_key(character_handler.key[23]) == "Armes"
    assert character_handler.convert_key(character_handler.key[24]) == "Joueur"


def test_mapping_display_list_info():
    db_handler = src.Database.DbHandler.DbHandler()
    db_handler.data = {"name": "kornettoh",
                       "settings": {"characters": [{"PLAYER": "123456789",
                                                    "NAME": "Chuck Norris",
                                                    "RACE": "God",
                                                    "JOB": "Soldier",
                                                    "EV": 12,
                                                    "EVMAX": 25,
                                                    "EA": 13,
                                                    "EAMAX": 26,
                                                    "COU": 12,
                                                    "INT": 13,
                                                    "CHA": 25,
                                                    "AD": 17,
                                                    "FO": 18,
                                                    "AT": 14,
                                                    "PRD": 19,
                                                    "DESTINY": 2,
                                                    "SKILLS": ["Ultra strengh", "Iron Fist"],
                                                    "GOLD": 152,
                                                    "SILVER": 23,
                                                    "BRONZE": 14,
                                                    "LEVEL": 2,
                                                    "SEX": "Homme",
                                                    "XP": 423,
                                                    "STUFF": ["Rope", "Potion"],
                                                    "WEAPONS": ["Left fist", "Right fist"]}]}}

    character_handler = src.CharacterDBHandler.CharacterDBHandler()
    character_handler.db_handler = db_handler
    character = character_handler.import_character("123456789")
    embed = character_handler.display_list_infos(0x00ff00,
                                                 [character_handler.DisplayItem(str(character.competences),
                                                                                character_handler.mapping["SKILLS"]),
                                                  character_handler.DisplayItem(character.race,
                                                                                character_handler.mapping["RACE"])],
                                                 "Title")
    assert embed.color == discord.colour.Color(0x00ff00)
    assert embed.title == "Title"
    assert len(embed.fields) == 2
    assert embed.fields[0].name == "Compétences"
    assert embed.fields[0].value == "['Ultra strengh', 'Iron Fist']"
    assert embed.fields[1].name == "Race"
    assert embed.fields[1].value == "God"


def test_mapping_char_stat_life_mana():
    db_handler = src.Database.DbHandler.DbHandler()
    db_handler.data = {"name": "kornettoh",
                       "settings": {"characters": [{"PLAYER": "123456789",
                                                    "NAME": "Chuck Norris",
                                                    "RACE": "God",
                                                    "JOB": "Soldier",
                                                    "EV": "12",
                                                    "EVMAX": "25",
                                                    "EA": "13",
                                                    "EAMAX": "26",
                                                    "COU": 12,
                                                    "INT": 13,
                                                    "CHA": 25,
                                                    "AD": 17,
                                                    "FO": 18,
                                                    "AT": 14,
                                                    "PRD": 19,
                                                    "DESTINY": 2,
                                                    "SKILLS": ["Ultra strengh", "Iron Fist"],
                                                    "GOLD": 152,
                                                    "SILVER": 23,
                                                    "BRONZE": 14,
                                                    "LEVEL": 2,
                                                    "SEX": "Homme",
                                                    "XP": 423,
                                                    "STUFF": ["Rope", "Potion"],
                                                    "WEAPONS": ["Left fist", "Right fist"]}]}}

    character_handler = src.CharacterDBHandler.CharacterDBHandler()
    character_handler.db_handler = db_handler
    character = character_handler.import_character("123456789")
    embed = character_handler.display_list_infos(0x00ff00,
                                                 [character_handler.DisplayItem(
                                                     character_handler.format_gauge(
                                                         character.ea,
                                                         character.ea_max),
                                                     character_handler.mapping["EA"]),
                                                     character_handler.DisplayItem(
                                                         character_handler.format_gauge(
                                                             character.ev,
                                                             character.ev_max),
                                                         character_handler.mapping["EV"])])
    assert embed.color == discord.colour.Color(0x00ff00)
    assert embed.title is None
    assert len(embed.fields) == 2
    assert embed.fields[0].name == "Energie astrale"
    assert embed.fields[0].value == "13/26"
    assert embed.fields[1].name == "Energie vitale"
    assert embed.fields[1].value == "12/25"


def test_display_char():
    db_handler = src.Database.DbHandler.DbHandler()
    db_handler.data = {"name": "kornettoh",
                       "settings": {"characters": [{"PLAYER": "123456789",
                                                    "NAME": "Chuck Norris",
                                                    "RACE": "God",
                                                    "JOB": "Soldier",
                                                    "EV": "12",
                                                    "EVMAX": "25",
                                                    "EA": "13",
                                                    "EAMAX": "26",
                                                    "COU": 12,
                                                    "INT": 13,
                                                    "CHA": 25,
                                                    "AD": 17,
                                                    "FO": 18,
                                                    "AT": 14,
                                                    "PRD": 19,
                                                    "DESTINY": 2,
                                                    "SKILLS": ["Ultra strengh", "Iron Fist"],
                                                    "GOLD": "152",
                                                    "SILVER": "23",
                                                    "BRONZE": "14",
                                                    "LEVEL": 2,
                                                    "SEX": "Homme",
                                                    "XP": 423,
                                                    "STUFF": ["Rope", "Potion"],
                                                    "WEAPONS": ["Left fist", "Right fist"]}]}}

    character_handler = src.CharacterDBHandler.CharacterDBHandler()
    character_handler.db_handler = db_handler
    character = character_handler.import_character("123456789")

    embed = character_handler.display_basic_infos(character)
    assert embed.color == discord.colour.Color(0x00ff00)
    assert embed.title == "Chuck Norris"
    assert len(embed.fields) == 5

    embed = character_handler.display_attack_info(character, True)
    assert embed.color == discord.colour.Color(0x00ff00)
    assert embed.title == "Chuck Norris"
    assert len(embed.fields) == 3
    embed = character_handler.display_attack_info(character)
    assert embed.color == discord.colour.Color(0x00ff00)
    assert embed.title is None
    assert len(embed.fields) == 3

    embed = character_handler.display_money_infos(character, True)
    assert embed.color == discord.colour.Color(0x00ff00)
    assert embed.title == "Chuck Norris"
    assert len(embed.fields) == 1
    assert embed.fields[0].name == "Pièces d'or"
    assert embed.fields[0].value == "152/23/14"
    embed = character_handler.display_money_infos(character)
    assert embed.color == discord.colour.Color(0x00ff00)
    assert embed.title is None
    assert len(embed.fields) == 1
    assert embed.fields[0].name == "Pièces d'or"
    assert embed.fields[0].value == "152/23/14"

    #Specific formatting
    embed = character_handler.display_minimum_info_character(character)
    assert len(embed) == 1
    assert embed[0].color == discord.colour.Color(0x00ff00)
    assert embed[0].title == "Chuck Norris"
    assert len(embed[0].fields) == 7

    embed = character_handler.display_skills_character(character)
    assert len(embed) == 1
    assert embed[0].color == discord.colour.Color(0x00ff00)
    assert embed[0].title == "Chuck Norris"
    assert len(embed[0].fields) == 1

    embed = character_handler.display_stuff_character(character)
    assert len(embed) == 1
    assert embed[0].color == discord.colour.Color(0x00ff00)
    assert embed[0].title == "Chuck Norris"
    assert len(embed[0].fields) == 1

    embed = character_handler.display_weapons_character(character)
    assert len(embed) == 1
    assert embed[0].color == discord.colour.Color(0x00ff00)
    assert embed[0].title == "Chuck Norris"
    assert len(embed[0].fields) == 1

    embed = character_handler.display_info_character(character)
    assert len(embed) == 5


def test_money_all_operations():
    src.Error.ErrorManager.ErrorManager().clear_error()
    db_handler = src.Database.DbHandler.DbHandler()
    db_handler.data = {"name": "kornettoh",
                       "settings": {"characters": [{"PLAYER": "123456789",
                                                    "NAME": "Chuck Norris",
                                                    "RACE": "God",
                                                    "JOB": "Soldier",
                                                    "EV": "12",
                                                    "EVMAX": "25",
                                                    "EA": "13",
                                                    "EAMAX": "26",
                                                    "COU": 12,
                                                    "INT": 13,
                                                    "CHA": 25,
                                                    "AD": 17,
                                                    "FO": 18,
                                                    "AT": 14,
                                                    "PRD": 19,
                                                    "DESTINY": 2,
                                                    "SKILLS": ["Ultra strengh", "Iron Fist"],
                                                    "GOLD": "152",
                                                    "SILVER": "23",
                                                    "BRONZE": "14",
                                                    "LEVEL": 2,
                                                    "SEX": "Homme",
                                                    "XP": 423,
                                                    "STUFF": ["Rope", "Potion"],
                                                    "WEAPONS": ["Left fist", "Right fist"]}]}}
    db_handler.update_game = MagicMock()

    character_handler = src.CharacterDBHandler.CharacterDBHandler()
    character_handler.db_handler = db_handler

    gold, silver, bronze = character_handler.money_operation("123456789", "-1/1/-20")
    assert (db_handler.data["settings"]["characters"][0]["GOLD"] == "151" == gold)
    assert (db_handler.data["settings"]["characters"][0]["SILVER"] == "24" == silver)
    assert (db_handler.data["settings"]["characters"][0]["BRONZE"] == "0" == bronze)
    assert (len(src.Error.ErrorManager.ErrorManager.error_log) == 0)


def test_money_gold_silver():
    src.Error.ErrorManager.ErrorManager().clear_error()
    db_handler = src.Database.DbHandler.DbHandler()
    db_handler.data = {"name": "kornettoh",
                       "settings": {"characters": [{"PLAYER": "123456789",
                                                    "NAME": "Chuck Norris",
                                                    "RACE": "God",
                                                    "JOB": "Soldier",
                                                    "EV": "12",
                                                    "EVMAX": "25",
                                                    "EA": "13",
                                                    "EAMAX": "26",
                                                    "COU": 12,
                                                    "INT": 13,
                                                    "CHA": 25,
                                                    "AD": 17,
                                                    "FO": 18,
                                                    "AT": 14,
                                                    "PRD": 19,
                                                    "DESTINY": 2,
                                                    "SKILLS": ["Ultra strengh", "Iron Fist"],
                                                    "GOLD": "152",
                                                    "SILVER": "23",
                                                    "BRONZE": "14",
                                                    "LEVEL": 2,
                                                    "SEX": "Homme",
                                                    "XP": 423,
                                                    "STUFF": ["Rope", "Potion"],
                                                    "WEAPONS": ["Left fist", "Right fist"]}]}}
    db_handler.update_game = MagicMock()

    character_handler = src.CharacterDBHandler.CharacterDBHandler()
    character_handler.db_handler = db_handler

    gold, silver, bronze = character_handler.money_operation("123456789", "-1/1")
    assert (db_handler.data["settings"]["characters"][0]["GOLD"] == "151" == gold)
    assert (db_handler.data["settings"]["characters"][0]["SILVER"] == "24" == silver)
    assert (db_handler.data["settings"]["characters"][0]["BRONZE"] == "14" == bronze)
    assert (len(src.Error.ErrorManager.ErrorManager.error_log) == 0)


def test_money_gold():
    src.Error.ErrorManager.ErrorManager().clear_error()
    db_handler = src.Database.DbHandler.DbHandler()
    db_handler.data = {"name": "kornettoh",
                       "settings": {"characters": [{"PLAYER": "123456789",
                                                    "NAME": "Chuck Norris",
                                                    "RACE": "God",
                                                    "JOB": "Soldier",
                                                    "EV": "12",
                                                    "EVMAX": "25",
                                                    "EA": "13",
                                                    "EAMAX": "26",
                                                    "COU": 12,
                                                    "INT": 13,
                                                    "CHA": 25,
                                                    "AD": 17,
                                                    "FO": 18,
                                                    "AT": 14,
                                                    "PRD": 19,
                                                    "DESTINY": 2,
                                                    "SKILLS": ["Ultra strengh", "Iron Fist"],
                                                    "GOLD": "152",
                                                    "SILVER": "23",
                                                    "BRONZE": "14",
                                                    "LEVEL": 2,
                                                    "SEX": "Homme",
                                                    "XP": 423,
                                                    "STUFF": ["Rope", "Potion"],
                                                    "WEAPONS": ["Left fist", "Right fist"]}]}}
    db_handler.update_game = MagicMock()

    character_handler = src.CharacterDBHandler.CharacterDBHandler()
    character_handler.db_handler = db_handler

    gold, silver, bronze = character_handler.money_operation("123456789", "-1")
    assert (db_handler.data["settings"]["characters"][0]["GOLD"] == "151" == gold)
    assert (db_handler.data["settings"]["characters"][0]["SILVER"] == "23" == silver)
    assert (db_handler.data["settings"]["characters"][0]["BRONZE"] == "14" == bronze)
    assert (len(src.Error.ErrorManager.ErrorManager.error_log) == 0)


def test_money_error():
    src.Error.ErrorManager.ErrorManager().clear_error()
    db_handler = src.Database.DbHandler.DbHandler()
    db_handler.data = {"name": "kornettoh",
                       "settings": {"characters": [{"PLAYER": "123456789",
                                                    "NAME": "Chuck Norris",
                                                    "RACE": "God",
                                                    "JOB": "Soldier",
                                                    "EV": "12",
                                                    "EVMAX": "25",
                                                    "EA": "13",
                                                    "EAMAX": "26",
                                                    "COU": 12,
                                                    "INT": 13,
                                                    "CHA": 25,
                                                    "AD": 17,
                                                    "FO": 18,
                                                    "AT": 14,
                                                    "PRD": 19,
                                                    "DESTINY": 2,
                                                    "SKILLS": ["Ultra strengh", "Iron Fist"],
                                                    "GOLD": "152",
                                                    "SILVER": "23",
                                                    "BRONZE": "14",
                                                    "LEVEL": 2,
                                                    "SEX": "Homme",
                                                    "XP": 423,
                                                    "STUFF": ["Rope", "Potion"],
                                                    "WEAPONS": ["Left fist", "Right fist"]}]}}

    character_handler = src.CharacterDBHandler.CharacterDBHandler()
    character_handler.db_handler = db_handler

    gold, silver, bronze = character_handler.money_operation("123456789", "toto")
    assert (db_handler.data["settings"]["characters"][0]["GOLD"] == "152")
    assert (db_handler.data["settings"]["characters"][0]["SILVER"] == "23")
    assert (db_handler.data["settings"]["characters"][0]["BRONZE"] == "14")
    assert ("Error" == gold == silver == bronze)
    assert (len(src.Error.ErrorManager.ErrorManager.error_log) == 1)
    assert src.Error.ErrorManager.ErrorManager.error_log[0].error_type ==\
        src.Error.ErrorManager.ErrorCode.NOT_AN_INTEGER


def test_money_error_with_db():
    src.Error.ErrorManager.ErrorManager().clear_error()
    db_handler = src.Database.DbHandler.DbHandler()
    db_handler.data = {"name": "kornettoh",
                       "settings": {"characters": [{"PLAYER": "123456789",
                                                    "NAME": "Chuck Norris",
                                                    "RACE": "God",
                                                    "JOB": "Soldier",
                                                    "EV": "12",
                                                    "EVMAX": "25",
                                                    "EA": "13",
                                                    "EAMAX": "26",
                                                    "COU": 12,
                                                    "INT": 13,
                                                    "CHA": 25,
                                                    "AD": 17,
                                                    "FO": 18,
                                                    "AT": 14,
                                                    "PRD": 19,
                                                    "DESTINY": 2,
                                                    "SKILLS": ["Ultra strengh", "Iron Fist"],
                                                    "GOLD": "152",
                                                    "SILVER": "23",
                                                    "BRONZE": "14",
                                                    "LEVEL": 2,
                                                    "SEX": "Homme",
                                                    "XP": 423,
                                                    "STUFF": ["Rope", "Potion"],
                                                    "WEAPONS": ["Left fist", "Right fist"]}]}}
    db_handler.update_game = MagicMock(return_value=False)
    src.Error.ErrorManager.ErrorManager().add_error(src.Error.ErrorManager.ErrorCode.NO_DOCUMENT_FOUND,
                                                    "update_game")

    character_handler = src.CharacterDBHandler.CharacterDBHandler()
    character_handler.db_handler = db_handler

    gold, silver, bronze = character_handler.money_operation("123456789", "-1")
    assert (db_handler.data["settings"]["characters"][0]["GOLD"] == "151")
    assert (db_handler.data["settings"]["characters"][0]["SILVER"] == "23")
    assert (db_handler.data["settings"]["characters"][0]["BRONZE"] == "14")
    assert ("Error" == gold == silver == bronze)
    assert (len(src.Error.ErrorManager.ErrorManager.error_log) == 1)
    assert src.Error.ErrorManager.ErrorManager.error_log[0].error_type ==\
        src.Error.ErrorManager.ErrorCode.NO_DOCUMENT_FOUND


def test_compute_ev():
    src.Error.ErrorManager.ErrorManager().clear_error()
    json = {"PLAYER": "123456789",
            "NAME": "Chuck Norris",
            "RACE": "God",
            "JOB": "Soldier",
            "EV": "12",
            "EVMAX": "25",
            "EA": "13",
            "EAMAX": "26",
            "COU": 12,
            "INT": 13,
            "CHA": 25,
            "AD": 17,
            "FO": 18,
            "AT": 14,
            "PRD": 19,
            "DESTINY": 2,
            "SKILLS": ["Ultra strengh", "Iron Fist"],
            "GOLD": "152",
            "SILVER": "23",
            "BRONZE": "14",
            "LEVEL": 2,
            "SEX": "Homme",
            "XP": 423,
            "STUFF": ["Rope", "Potion"],
            "WEAPONS": ["Left fist", "Right fist"]}

    character_handler = src.CharacterDBHandler.CharacterDBHandler()

    assert character_handler.compute_ev(1, json)
    assert json["EV"] == "13"

    assert character_handler.compute_ev(-1, json)
    assert json["EV"] == "12"

    assert character_handler.compute_ev(100, json)
    assert json["EV"] == "25"

    assert character_handler.compute_ev(-100, json)
    assert json["EV"] == "0"

    assert character_handler.compute_ev(-100, json)
    assert json["EV"] == "0"

    json["EV"] = "toto"
    assert not character_handler.compute_ev(-100, json)
    assert len(src.Error.ErrorManager.ErrorManager.error_log)
    assert src.Error.ErrorManager.ErrorManager.error_log[0].error_type ==\
        src.Error.ErrorManager.ErrorCode.NOT_AN_INTEGER
