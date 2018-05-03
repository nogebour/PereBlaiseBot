import discord
from enum import Enum

from .Database.DbHandler import DbHandler
from .Error.ErrorManager import ErrorManager, ErrorCode

class Character:

    def __init__(self):
        self.userName = None
        self.name = None
        self.job = None
        self.ev = None
        self.ev_max = None
        self.ea = None
        self.ea_max = None
        self.courage = None
        self.intelligence = None
        self.charisme = None
        self.adresse = None
        self.force = None
        self.attaque = None
        self.parade = None
        self.pointsDeDestin = None
        self.competences = []
        self.piecesOr = None
        self.piecesArgent = None
        self.piecesBronze = None
        self.niveau = None
        self.sexe = None
        self.experience = None
        self.stuff = []
        self.weapons = []


class CharacterDBHandler:
    def __init__(self):
        self.db_handler = DbHandler()
        self.data = None
        self.key = ["RACE",
                    "JOB",
                    "EV",
                    "EVMAX",
                    "EA",
                    "EAMAX",
                    "COU",
                    "INT",
                    "CHA",
                    "AD",
                    "FO",
                    "AT",
                    "PRD",
                    "DESTINY",
                    "SKILLS",
                    "GOLD",
                    "SILVER",
                    "BRONZE",
                    "LEVEL",
                    "SEX",
                    "XP",
                    "NAME",
                    "STUFF",
                    "WEAPONS",
                    "PLAYER"]
        self.mapping = {self.key[0]: "Race",
                        self.key[1]: "Métier",
                        self.key[2]: "Energie vitale",
                        self.key[3]: "Energie vitale maximale",
                        self.key[4]: "Energie astrale",
                        self.key[5]: "Energie astrale maximale",
                        self.key[6]: "Courage",
                        self.key[7]: "Intelligence",
                        self.key[8]: "Charisme",
                        self.key[9]: "Adresse",
                        self.key[10]: "Force",
                        self.key[11]: "Attaque",
                        self.key[12]: "Parade",
                        self.key[13]: "Points de destin",
                        self.key[14]: "Compétences",
                        self.key[15]: "Pièces d'or",
                        self.key[16]: "Pièces d'argent",
                        self.key[17]: "Pièces de bronze",
                        self.key[18]: "Niveau",
                        self.key[19]: "Sexe",
                        self.key[20]: "Points d'expérience",
                        self.key[21]: "Nom",
                        self.key[22]: "Equipement",
                        self.key[23]: "Armes",
                        self.key[24]: "Joueur"}

    class DisplayItem:
        def __init__(self, value, label):
            self.value = value
            self.label = label

    def initialize(self):
        self.db_handler.retrieve_game()
        self.data = self.db_handler.data

    def import_character(self, user_name):
        values = self.db_handler.read_file_for_character(user_name)
        new_character = Character()
        new_character.userName = values["PLAYER"]
        new_character.name = values["NAME"]
        new_character.race = values["RACE"]
        new_character.job = values["JOB"]
        new_character.ev = values["EV"]
        new_character.ev_max = values["EVMAX"]
        new_character.ea = values["EA"]
        new_character.ea_max = values["EAMAX"]
        new_character.courage = values["COU"]
        new_character.intelligence = values["INT"]
        new_character.charisme = values["CHA"]
        new_character.adresse = values["AD"]
        new_character.force = values["FO"]
        new_character.attaque = values["AT"]
        new_character.parade = values["PRD"]
        new_character.pointsDeDestin = values["DESTINY"]
        new_character.competences = values["SKILLS"]
        new_character.piecesOr = values["GOLD"]
        new_character.piecesArgent = values["SILVER"]
        new_character.piecesBronze = values["BRONZE"]
        new_character.niveau = values["LEVEL"]
        new_character.sexe = values["SEX"]
        new_character.experience = values["XP"]
        new_character.stuff = values["STUFF"]
        new_character.weapons = values["WEAPONS"]
        return new_character

    def convert_key(self, key):
        return self.mapping[key]

    def display_basic_infos(self, character):
        return self.display_list_infos(0x00ff00,
                                       [self.DisplayItem(character.race, self.mapping["RACE"]),
                                        self.DisplayItem(character.job, self.mapping["JOB"]),
                                        self.DisplayItem(character.sexe, self.mapping["SEX"]),
                                        self.DisplayItem(character.niveau, self.mapping["LEVEL"]),
                                        self.DisplayItem(character.experience, self.mapping["XP"])],
                                       character.name)

    def display_basic_stats(self, character, display_name=False):
        return self.display_list_infos(0x00ff00,
                                       [self.DisplayItem(self.format_gauge(character.ev,
                                                                           character.ev_max),
                                                         self.mapping["EV"]),
                                        self.DisplayItem(self.format_gauge(character.ea,
                                                                           character.ea_max),
                                                         self.mapping["EA"]),
                                        self.DisplayItem(character.pointsDeDestin,
                                                         self.mapping["DESTINY"]),
                                        self.DisplayItem(self.format_money(character.piecesOr,
                                                                           character.piecesArgent,
                                                                           character.piecesBronze),
                                                         self.mapping["GOLD"]),
                                        self.DisplayItem(character.attaque,
                                                         self.mapping["AT"]),
                                        self.DisplayItem(character.parade,
                                                         self.mapping["PRD"]),
                                        self.DisplayItem(character.adresse,
                                                         self.mapping["AD"])],
                                       (character.name if display_name else None))

    def display_attack_info(self, character, display_name=False):
        return self.display_list_infos(0x00ff00,
                                       [self.DisplayItem(character.attaque, self.mapping["AT"]),
                                        self.DisplayItem(character.parade, self.mapping["PRD"]),
                                        self.DisplayItem(character.adresse, self.mapping["AD"])],
                                       (character.name if display_name else None))

    def display_money_infos(self, character, display_name=False):
        return self.display_list_infos(0x00ff00,
                                       [self.DisplayItem(self.format_money(character.piecesOr,
                                                                           character.piecesArgent,
                                                                           character.piecesBronze),
                                                         self.mapping["GOLD"])],
                                       (character.name if display_name else None))

    def display_skills(self, character, display_name=False):
        return self.display_list_infos(0x00ff00,
                                       [self.DisplayItem(str(character.competences), self.mapping["SKILLS"])],
                                       (character.name if display_name else None))

    def display_stuff(self, character, display_name=False):
        return self.display_list_infos(0x00ff00,
                                       [self.DisplayItem(str(character.stuff), self.mapping["STUFF"])],
                                       (character.name if display_name else None))

    def display_weapons(self, character, display_name=False):
        return self.display_list_infos(0x00ff00,
                                       [self.DisplayItem(str(character.weapons), self.mapping["WEAPONS"])],
                                       (character.name if display_name else None))

    def format_gauge(self, value, max_value, min_value=0):
        return str(max(int(value), int(min_value)))+"/"+str(max_value)

    def format_money(self, gold, silver, bronze):
        return str(gold)+"/"+str(silver)+"/"+str(bronze)

    def display_list_infos(self, color, list_stats, title=None):
        embed_formated = discord.Embed(color=color, title=title)
        for stat in list_stats:
            embed_formated.add_field(
                name=stat.label,
                value=stat.value,
                inline=True)
        return embed_formated

    def display_minimum_info_character(self, character):
        embeds = [self.display_basic_stats(character, True)]
        return embeds

    def display_weapons_character(self, character):
        embeds = [self.display_weapons(character, True)]
        return embeds

    def display_stuff_character(self, character):
        embeds = [self.display_stuff(character, True)]
        return embeds

    def display_skills_character(self, character):
        embeds = [self.display_skills(character, True)]
        return embeds

    def display_info_character(self, character):
        embeds = [self.display_basic_infos(character),
                  self.display_basic_stats(character),
                  self.display_skills(character),
                  self.display_stuff(character),
                  self.display_weapons(character)]
        return embeds

    def money_operation(self, username, amount):
        the_char = self.db_handler.read_file_for_character(username)
        operations = amount.split("/")
        try:
            if len(operations) >= 1:
                tmp_gold = int(the_char["GOLD"]) + int(operations[0])
                if tmp_gold < 0:
                    tmp_gold = 0
                the_char["GOLD"] = str(tmp_gold)
            if len(operations) >= 2:
                tmp_silver = int(the_char["SILVER"]) + int(operations[1])
                if tmp_silver < 0:
                    tmp_silver = 0
                the_char["SILVER"] = str(tmp_silver)
            if len(operations) >= 3:
                tmp_bronze = int(the_char["BRONZE"]) + int(operations[2])
                if tmp_bronze < 0:
                    tmp_bronze = 0
                the_char["BRONZE"] = str(tmp_bronze)
            if self.db_handler.update_game():
                return the_char["GOLD"], the_char["SILVER"], the_char["BRONZE"]
        except ValueError:
            ErrorManager().add_error(ErrorCode.NOT_AN_INTEGER, "money_operation")
        return "Error", "Error", "Error"

    def increase_ev(self, user_name, amount):
        char_sheet = self.db_handler.read_file_for_character(user_name)
        self.compute_ev(amount, char_sheet)
        self.db_handler.update_game()
        return char_sheet["EV"]

    def compute_ev(self, amount, char_sheet):
        try:
            ev = int(char_sheet["EV"])
            ev_max = int(char_sheet["EVMAX"])
        except ValueError:
            ErrorManager().add_error(ErrorCode.NOT_AN_INTEGER, "compute_ev")
            return False

        tmp_ev = ev + amount
        if tmp_ev > ev_max:
            tmp_ev = ev_max
        if tmp_ev < 0:
            tmp_ev = 0
        char_sheet["EV"] = str(tmp_ev)
        return True

    def decrease_ev(self, user_name, amount):
        return self.increase_ev(user_name, (0 - amount))

    def increase_ev_group(self, amount):
        print("increase")
        result = []
        for player in self.db_handler.data['settings']['characters']:
            print("Decrease player" + player["PLAYER"])
            self.compute_ev(amount, player)
            result.append({'id': player["PLAYER"], 'remainingLife': player["EV"]})
        print('Save Changes')
        self.db_handler.update_game()
        return result

    def decrease_ev_group(self, amount):
        print("Decrease")
        return self.increase_ev_group((0 - amount))
