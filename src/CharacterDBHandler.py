import discord

from src.DbHandler import DbHandler


class CharacterV2:
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
        self.mapping = {self.key[0]:"Race",
                        self.key[1]:"Métier",
                        self.key[2]:"Energie vitale",
                        self.key[3]:"Energie vitale maximale",
                        self.key[4]:"Energie astrale",
                        self.key[5]:"Energie astrale maximale",
                        self.key[6]:"Courage",
                        self.key[7]:"Intelligence",
                        self.key[8]:"Charisme",
                        self.key[9]:"Adresse",
                        self.key[10]:"Force",
                        self.key[11]:"Attaque",
                        self.key[12]:"Parade",
                        self.key[13]:"Points de destin",
                        self.key[14]:"Compétences",
                        self.key[15]:"Pièces d'or",
                        self.key[16]:"Pièces d'argent",
                        self.key[17]:"Pièces de bronze",
                        self.key[18]:"Niveau",
                        self.key[19]:"Sexe",
                        self.key[20]:"Points d'expérience",
                        self.key[21]:"Nom",
                        self.key[22]:"Equipement",
                        self.key[23]:"Armes",
                        self.key[23]:"Joueur"}

    def initialize(self):
        self.dbHandler.retrieve_game()
        self.data = self.dbHandler.data

    def mappingCharStat(self, aKey, aChar):
        if aKey==self.key[0]:
            return aChar.race
        elif aKey==self.key[1]:
            return aChar.job
        elif aKey==self.key[2]:
            return aChar.ev
        elif aKey==self.key[3]:
            return aChar.evMax
        elif aKey==self.key[4]:
            return aChar.ea
        elif aKey==self.key[5]:
            return aChar.eaMax
        elif aKey==self.key[6]:
            return aChar.courage
        elif aKey==self.key[7]:
            return aChar.intelligence
        elif aKey==self.key[8]:
            return aChar.charisme
        elif aKey==self.key[9]:
            return aChar.adresse
        elif aKey==self.key[10]:
            return aChar.force
        elif aKey==self.key[11]:
            return aChar.attaque
        elif aKey==self.key[12]:
            return aChar.parade
        elif aKey==self.key[13]:
            return aChar.pointsDeDestin
        elif aKey==self.key[14]:
            return str(aChar.competences)
        elif aKey==self.key[15]:
            return aChar.piecesOr
        elif aKey==self.key[16]:
            return aChar.piecesArgent
        elif aKey==self.key[17]:
            return aChar.piecesBronze
        elif aKey==self.key[18]:
            return aChar.niveau
        elif aKey==self.key[19]:
            return aChar.sexe
        elif aKey==self.key[20]:
            return aChar.experience
        elif aKey==self.key[21]:
            return aChar.name
        elif aKey==self.key[22]:
            return str(aChar.stuff)
        elif aKey==self.key[23]:
            return str(aChar.weapons)
        elif aKey==self.key[24]:
            return str(aChar.userName)

    def readFileForCharacter(self,userId):
        for aPlayer in self.data['settings']['characters']:
            if aPlayer["PLAYER"] == userId:
                return aPlayer

    def importCharacter(self, userName):
        values = self.readFileForCharacter(userName)
        aNewCharacter = CharacterV2()
        aNewCharacter.userName = values["PLAYER"]
        aNewCharacter.name = values["NAME"]
        aNewCharacter.name = values["NAME"]
        aNewCharacter.race = values["RACE"]
        aNewCharacter.job = values["JOB"]
        aNewCharacter.ev = values["EV"]
        aNewCharacter.evMax = values["EVMAX"]
        aNewCharacter.ea = values["EA"]
        aNewCharacter.eaMax = values["EAMAX"]
        aNewCharacter.courage = values["COU"]
        aNewCharacter.intelligence = values["INT"]
        aNewCharacter.charisme = values["CHA"]
        aNewCharacter.adresse = values["AD"]
        aNewCharacter.force = values["FO"]
        aNewCharacter.attaque = values["AT"]
        aNewCharacter.parade = values["PRD"]
        aNewCharacter.pointsDeDestin = values["DESTINY"]
        aNewCharacter.competences = values["SKILLS"]
        aNewCharacter.piecesOr = values["GOLD"]
        aNewCharacter.piecesArgent = values["SILVER"]
        aNewCharacter.piecesBronze = values["BRONZE"]
        aNewCharacter.niveau = values["LEVEL"]
        aNewCharacter.sexe = values["SEX"]
        aNewCharacter.experience= values["XP"]
        aNewCharacter.stuff = values["STUFF"]
        aNewCharacter.weapons = values["WEAPONS"]
        return aNewCharacter

    def convertKey(self, aKey):
        return self.mapping[aKey]

    def displayBasicInfos(self, aCharacter):
        return self.displayListOfInfos(0x00ff00, aCharacter, ["RACE","JOB","SEX","LEVEL","XP"], aCharacter.name)

    def displayBasicStats(self, aCharacter, displayName=False):
        return self.displayListOfInfos(0x00ff00, aCharacter, ["EV","EA","DESTINY","GOLD","AT","PRD","AD"], (aCharacter.name if displayName else None))

    def displayAttackInfo(self, aCharacter, displayName=False):
        return self.displayListOfInfos(0x00ff00, aCharacter, ["AT","PRD","AD"], (aCharacter.name if displayName else None))

    def displayMoneyInfos(self, aCharacter, displayName=False):
        return self.displayListOfInfos(0x00ff00, aCharacter, ["GOLD"], (aCharacter.name if displayName else None))

    def displaySkills(self, aCharacter, displayName=False):
        return self.displayListOfInfos(0x00ff00, aCharacter, ["SKILLS"], (aCharacter.name if displayName else None))

    def displayStuff(self, aCharacter, displayName=False):
        return self.displayListOfInfos(0x00ff00, aCharacter, ["STUFF"], (aCharacter.name if displayName else None))

    def displayWeapons(self, aCharacter, displayName=False):
        return self.displayListOfInfos(0x00ff00, aCharacter, ["WEAPONS"], (aCharacter.name if displayName else None))

    def displayListOfInfos(self, color, aCharacter, listOfStats, title=None):
        embedFormated = discord.Embed(color=color, title=title)
        for aStat in listOfStats:
            strValue = self.mappingCharStat(aStat, aCharacter)
            if(aStat == "EA"  or aStat == "EV"):
                strValue = (self.mappingCharStat(aStat, aCharacter) + "/" + self.mappingCharStat(aStat+"MAX", aCharacter))
            elif aStat == "GOLD":
                strValue = (self.mappingCharStat("GOLD", aCharacter) + "/" + self.mappingCharStat("SILVER", aCharacter) + "/" + self.mappingCharStat("BRONZE", aCharacter))
            embedFormated.add_field(
                name = self.mapping[aStat],
                value = strValue,
                inline = True)
        return embedFormated

    def displayMinimumInfoCharacter(self, aCharacter):
        embeds = [self.displayBasicStats(aCharacter,True)]
        return embeds

    def displayWeaponsCharacter(self, aCharacter):
        embeds = [self.displayWeapons(aCharacter, True)]
        return embeds

    def displayStuffCharacter(self, aCharacter):
        embeds = [self.displayStuff(aCharacter, True)]
        return embeds

    def displaySkillsCharacter(self, aCharacter):
        embeds = [self.displaySkills(aCharacter, True)]
        return embeds

    def displayInfoCharacter(self, aCharacter):
        embeds = [self.displayListOfInfos(0x00ff00, aCharacter, ["RACE","JOB","SEX","GOLD","LEVEL","XP"]),
                  self.displayListOfInfos(0x00ff00, aCharacter, ["EV","EA","DESTINY"]),
                  self.displayListOfInfos(0x00ff00, aCharacter, ["AT","PRD","AD"]),
                  self.displayListOfInfos(0x00ff00, aCharacter, ["SKILLS","STUFF","WEAPONS"])]
        return embeds

    def moneyOperation(self, userName, amount):
        theChar = self.readFileForCharacter(userName)
        print(theChar)
        operations = amount.split("/")
        if len(operations) >= 1:
            tempOr = int(theChar["GOLD"]) + int(operations[0])
            if(tempOr < 0):
                tempOr = 0
            theChar["GOLD"] = str(tempOr)
        if len(operations) >= 2:
            tempArgent = int(theChar["SILVER"]) + int(operations[1])
            if(tempArgent < 0):
                tempArgent = 0
            theChar["SILVER"] = str(tempArgent)
        if len(operations) >= 3:
            tempBronze = int(theChar["BRONZE"]) + int(operations[2])
            if(tempBronze < 0):
                tempBronze = 0
            theChar["BRONZE"] = str(tempBronze)
        self.dbHandler.update_game()
        return theChar["GOLD"], theChar["SILVER"], theChar["BRONZE"]

    def increaseEv(self, userName, amount):
        theCharSheet = self.readFileForCharacter(userName)
        tempEv = int(theCharSheet["EV"]) + amount
        if(tempEv > int(theCharSheet["EVMAX"])):
            tempEv = int(theCharSheet["EVMAX"])
        if(tempEv < 0):
            tempEv = 0
        theCharSheet["EV"] = str(tempEv)
        self.dbHandler.update_game()
        return theCharSheet["EV"]

    def decreaseEv(self, userName, amount):
        return self.increaseEv(userName, (0-amount))

    def increaseEvGroup(self, amount):
        print("increase")
        result = []
        for aPlayer in self.dbHandler.data['settings']['characters']:
            print("Decrease player" + aPlayer["PLAYER"])
            tempEv = int(aPlayer["EV"]) + amount
            if(tempEv > int(aPlayer["EVMAX"])):
                tempEv = int(aPlayer["EVMAX"])
            if(tempEv < 0):
                tempEv = 0
            aPlayer["EV"] = str(tempEv)
            result.append({'id': aPlayer["PLAYER"], 'remainingLife': aPlayer["EV"]})
        print('Save Changes')
        self.dbHandler.update_game()
        return result

    def decreaseEvGroup(self, amount):
        print("Decrease")
        return self.increaseEvGroup((0-amount))
