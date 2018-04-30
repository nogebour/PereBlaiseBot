from datetime import datetime, timedelta

from src.CharacterDBHandler import CharacterDBHandler
from src.DbHandler import DbHandler


class SettingsHandler:
    data = None
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

    def initialize(self):
        self.dbHandler.retrieve_game()
        self.data = self.dbHandler.data
        self.fill_data()

    def fill_data(self):
        self.start_time = datetime.strptime(self.data[self.key_settings][self.key_start_time], self.pattern)
        self.current_time = datetime.strptime(self.data[self.key_settings][self.key_current_time], self.pattern)
        self.players = self.data[self.key_settings][self.key_players]

    def get_elapsed_time(self):
        return self.current_time - self.start_time

    def add_time(self, delta):
        a_time_delta = timedelta(minutes=delta)
        self.current_time += a_time_delta
        return self.current_time

    def save_settings(self):
        self.data[self.key_settings][self.key_current_time] = self.current_time.strftime(self.pattern)
        self.dbHandler.update_game()
        #TODO Improve result handling

    # 'normal','bon','excellent'
    def handle_rest(self, quality, length, embed):
        db_handler = CharacterDBHandler()
        delta = 0
        try:
            delta = int(length)
        except ValueError:
            print("Not an integer")
            return False
        heal = 0
        if delta > 540:
            delta = 540
        if quality == "normal":
            heal = (delta / 240)
        elif quality == "bon":
            heal = (delta / 120)
        elif quality == "excellent":
            heal = (delta / 60)
        else:
            embed.add_field(value="Choix entre  'normal'|'bon'|'excellent'")
            return False
        players = db_handler.increaseEvGroup(int(heal))
        for a_player in players:
            embed.add_field(
                name= "Soin enregistrée",
                value="Le joueur <@" + a_player['id'] + "> a soigné " + str(int(heal)) + " points de vie.\nIl reste " +
                      a_player['remainingLife'] + " points de vie.",
                inline=False)
        return True

    def handle_walk(self, rythme, length, embed):
        db_handler = CharacterDBHandler()
        delta = 0
        try:
            delta = int(length)
        except ValueError:
            print("Not an integer")
            return False
        injury = 0
        if delta > 480:
            injury += (1+(delta-480)/60)
        if rythme == "normale":
            injury += 0
        elif rythme == "rapide":
            injury += (delta / (240)) + 1
        elif rythme == "barbare":
            injury += (delta / (120)) + 1
        else:
            embed.add_field(value="Choix entre 'normale'|'rapide'|'barbare'")
            return False
        players = db_handler.decreaseEvGroup(int(injury))
        for a_player in players:
            embed.add_field(
                name= "Blessure enregistrée",
                value="Le joueur <@" + a_player['id'] + "> a pris " + str(int(injury)) +
                      " points de dégats.\nIl reste " + a_player['remainingLife'] + " points de vie.",
                inline=False)
        return True

