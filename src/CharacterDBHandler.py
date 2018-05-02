import discord

from src.Database.DbHandler import DbHandler


class Character:
    userName = None
    name = None
    job = None
    ev = None
    evMax = None
    ea = None
    eaMax = None
    courage = None
    intelligence = None
    charisme = None
    adresse = None
    force = None
    attaque = None
    parade = None
    pointsDeDestin = None
    competences = []
    piecesOr = None
    piecesArgent = None
    piecesBronze = None
    niveau = None
    sexe = None
    experience = None
    stuff = []
    weapons = []


class CharacterDBHandler:
    def __init__(self):
        self.dbHandler = DbHandler()
        self.data = None
        self.key = ["RACE", "JOB", "EV", "EVMAX", "EA", "EAMAX", "COU", "INT", "CHA", "AD", "FO", "AT", "PRD", "DESTINY", "SKILLS", "GOLD", "SILVER", "BRONZE", "LEVEL", "SEX", "XP", "NAME", "STUFF", "WEAPONS", "PLAYER"]
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
                        self.key[23]: "Joueur"}

    def initialize(self):
        self.dbHandler.retrieve_game()
        self.data = self.dbHandler.data

    def mappingCharStat(self, key, character):
        if key == self.key[0]:
            return character.race
        elif key == self.key[1]:
            return character.job
        elif key == self.key[2]:
            return character.ev
        elif key == self.key[3]:
            return character.evMax
        elif key == self.key[4]:
            return character.ea
        elif key == self.key[5]:
            return character.eaMax
        elif key == self.key[6]:
            return character.courage
        elif key == self.key[7]:
            return character.intelligence
        elif key == self.key[8]:
            return character.charisme
        elif key == self.key[9]:
            return character.adresse
        elif key == self.key[10]:
            return character.force
        elif key == self.key[11]:
            return character.attaque
        elif key == self.key[12]:
            return character.parade
        elif key == self.key[13]:
            return character.pointsDeDestin
        elif key == self.key[14]:
            return str(character.competences)
        elif key == self.key[15]:
            return character.piecesOr
        elif key == self.key[16]:
            return character.piecesArgent
        elif key == self.key[17]:
            return character.piecesBronze
        elif key == self.key[18]:
            return character.niveau
        elif key == self.key[19]:
            return character.sexe
        elif key == self.key[20]:
            return character.experience
        elif key == self.key[21]:
            return character.name
        elif key == self.key[22]:
            return str(character.stuff)
        elif key == self.key[23]:
            return str(character.weapons)
        elif key == self.key[24]:
            return str(character.userName)

    def import_character(self, user_name):
        values = self.dbHandler.read_file_for_character(user_name)
        new_character = Character()
        new_character.userName = values["PLAYER"]
        new_character.name = values["NAME"]
        new_character.name = values["NAME"]
        new_character.race = values["RACE"]
        new_character.job = values["JOB"]
        new_character.ev = values["EV"]
        new_character.evMax = values["EVMAX"]
        new_character.ea = values["EA"]
        new_character.eaMax = values["EAMAX"]
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
        return self.display_list_infos(0x00ff00, character, ["RACE", "JOB", "SEX", "LEVEL", "XP"], character.name)

    def display_basic_stats(self, character, display_name=False):
        return self.display_list_infos(0x00ff00, character, ["EV", "EA", "DESTINY", "GOLD", "AT", "PRD", "AD"], (character.name if display_name else None))

    def display_attack_info(self, character, display_name=False):
        return self.display_list_infos(0x00ff00, character, ["AT", "PRD", "AD"], (character.name if display_name else None))

    def display_money_infos(self, character, display_name=False):
        return self.display_list_infos(0x00ff00, character, ["GOLD"], (character.name if display_name else None))

    def display_skills(self, character, display_name=False):
        return self.display_list_infos(0x00ff00, character, ["SKILLS"], (character.name if display_name else None))

    def display_stuff(self, character, display_name=False):
        return self.display_list_infos(0x00ff00, character, ["STUFF"], (character.name if display_name else None))

    def display_weapons(self, character, display_name=False):
        return self.display_list_infos(0x00ff00, character, ["WEAPONS"], (character.name if display_name else None))

    def display_list_infos(self, color, character, list_stats, title=None):
        embed_formated = discord.Embed(color=color, title=title)
        for stat in list_stats:
            str_value = self.mappingCharStat(stat, character)
            if stat == "EA" or stat == "EV":
                str_value = (self.mappingCharStat(stat, character) + "/" + self.mappingCharStat(stat+"MAX", character))
            elif stat == "GOLD":
                str_value = (self.mappingCharStat("GOLD", character) + "/" + self.mappingCharStat("SILVER", character) +
                             "/" + self.mappingCharStat("BRONZE", character))
            embed_formated.add_field(
                name=self.mapping[stat],
                value=str_value,
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
        embeds = [self.display_list_infos(0x00ff00, character, ["RACE", "JOB", "SEX", "GOLD", "LEVEL", "XP"]),
                  self.display_list_infos(0x00ff00, character, ["EV", "EA", "DESTINY"]),
                  self.display_list_infos(0x00ff00, character, ["AT", "PRD", "AD"]),
                  self.display_list_infos(0x00ff00, character, ["SKILLS", "STUFF", "WEAPONS"])]
        return embeds

    def money_operation(self, username, amount):
        the_char = self.dbHandler.read_file_for_character(username)
        print(the_char)
        operations = amount.split("/")
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
        self.dbHandler.update_game()
        return the_char["GOLD"], the_char["SILVER"], the_char["BRONZE"]

    def increase_ev(self, user_name, amount):
        char_sheet = self.dbHandler.read_file_for_character(user_name)
        tmp_ev = int(char_sheet["EV"]) + amount
        if tmp_ev > int(char_sheet["EVMAX"]):
            tmp_ev = int(char_sheet["EVMAX"])
        if tmp_ev < 0:
            tmp_ev = 0
        char_sheet["EV"] = str(tmp_ev)
        self.dbHandler.update_game()
        return char_sheet["EV"]

    def decrease_ev(self, user_name, amount):
        return self.increase_ev(user_name, (0 - amount))

    def increase_ev_group(self, amount):
        print("increase")
        result = []
        for player in self.dbHandler.data['settings']['characters']:
            print("Decrease player" + player["PLAYER"])
            temp_ev = int(player["EV"]) + amount
            if temp_ev > int(player["EVMAX"]):
                temp_ev = int(player["EVMAX"])
            if temp_ev < 0:
                temp_ev = 0
            player["EV"] = str(temp_ev)
            result.append({'id': player["PLAYER"], 'remainingLife': player["EV"]})
        print('Save Changes')
        self.dbHandler.update_game()
        return result

    def decrease_ev_group(self, amount):
        print("Decrease")
        return self.increase_ev_group((0 - amount))
