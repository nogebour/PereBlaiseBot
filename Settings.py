from datetime import datetime, timedelta
from CharacterDBHandler import CharacterDBHandler
from DbHandler import DbHandler

class SettingsHandler:
    dbHandler = None
    pattern = "%d/%m/%Y - %H:%M"
    key_start_time = "start_time"
    key_current_time = "current_time"
    key_players = "players"
    key_settings = 'settings'
    start_time = datetime.now()
    current_time = datetime.now()
    players = []
    def __init__(self):
        self.dbHandler = DbHandler()
        self.data = self.dbHandler.data
        self.fillData()

    def fillData(self):
        self.start_time = datetime.strptime(self.data[self.key_settings][self.key_start_time], self.pattern)
        self.current_time = datetime.strptime(self.data[self.key_settings][self.key_current_time], self.pattern)
        self.players = self.data[self.key_settings][self.key_players]

    def getElapsedTime(self):
        return (self.current_time - self.start_time)

    def addTime(self, delta):
        aTimeDelta = timedelta(minutes=delta)
        self.current_time+=aTimeDelta
        return  self.current_time

    def saveSettings(self):
        self.data[self.key_settings][self.key_current_time] = self.current_time.strftime(self.pattern)
        self.dbHandler.updateGame()

            #'normal','bon','excellent'
    def handleRest(self, quality, length, embed):
        aDbHandler = CharacterDBHandler()
        delta = 0
        try:
            delta = int(length)
        except ValueError:
            print("Not an integer")
            return False
        heal = 0
        if delta > 540:
            delta = 540
        if (quality == "normal"):
            heal = (delta / 240)
        elif (quality == "bon"):
            heal = (delta / 120)
        elif(quality == "excellent"):
            heal = (delta / 60)
        else:
            embed.add_field(value="Choix entre  'normal'|'bon'|'excellent'")
            return False
        print ("Debug")
        players = aDbHandler.increaseEvGroup(int(heal))
        for aPlayer in players:
            embed.add_field(
                name=("Soin enregistrée"),
                value="Le joueur <@" + aPlayer['id'] + "> a soigné " + str(heal) + " points de vie.\nIl reste " + aPlayer['remainingLife'] + " points de vie.",
                inline=False)
        return True

    def handleWalk(self, rythme, length, embed):
        aDbHandler = CharacterDBHandler()
        delta = 0
        try:
            delta = int(length)
        except ValueError:
            print("Not an integer")
            return False
        injury = 0
        if delta > 480:
            injury +=(1+(delta-480)/60)
        if (rythme == "normale"):
            injury += 0
        elif (rythme == "rapide"):
            injury += (delta / (240)) + 1
        elif(rythme == "barbare"):
            injury += (delta / (120)) + 1
        else:
            embed.add_field(value="Choix entre  'normale'|'rapide'|'barbare'")
            return False
        players = aDbHandler.decreaseEvGroup(int(injury))
        for aPlayer in players:
            embed.add_field(
                name=("Soin enregistrée"),
                value="Le joueur <@" + aPlayer['id'] + "> a pris " + str(injury) + " points de dégats.\nIl reste " + aPlayer['remainingLife'] + " points de vie.",
                inline=False)
        return True

