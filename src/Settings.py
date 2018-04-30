from datetime import datetime, timedelta

from src.CharacterDBHandler import CharacterDBHandler
from src.DbHandler import DbHandler


class SettingsHandler:
    pattern = "%d/%m/%Y - %H:%M"
    key_start_time = "start_time"
    key_current_time = "current_time"
    key_players = "players"
    key_settings = 'settings'

    def __init__(self):
        self.data = None
        self.db_handler = None
        self.error_log = []
        self.start_time = datetime.now()
        self.current_time = datetime.now()
        self.players = []
        self.db_handler = DbHandler()

    def initialize(self):
        self.db_handler.retrieve_game()
        self.data = self.db_handler.data
        self.fill_data()

    def fill_data(self):  # TODO Improve way of handling non-present date
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
        self.db_handler.update_game()
        #TODO Improve result handling

    # 'normal','bon','excellent'
    def compute_rest(self, quality, delta):
        if delta > 540:
            delta = 540
        if quality == "normal":
            return int(delta / 240)
        elif quality == "bon":
            return int(delta / 120)
        elif quality == "excellent":
            return int(delta / 60)
        else:
            self.error_log.append({"error_code": 3,
                                   "error_msg": "Invalid rest quality",
                                   "context": "compute_rest",
                                   "timestamp": datetime.now()})
            raise ValueError("Choix entre 'normal'|'bon'|'excellent'")

    # 'normale','rapide','barbare'
    def compute_walk(self, speed, delta):
        injury = 0
        if delta > 480:
            injury += int(1+(delta-480)/60)
        if speed == "normale":
            injury += 0
        elif speed == "rapide":
            injury += int(delta / 240) + 1
        elif speed == "barbare":
            injury += int(delta / 120) + 1
        else:
            self.error_log.append({"error_code": 4,
                                   "error_msg": "Invalid walk speed",
                                   "context": "compute_walk",
                                   "timestamp": datetime.now()})
            raise ValueError("Choix entre 'normale'|'rapide'|'barbare'")
        return injury

    def handle_rest(self, quality, length, embed):
        db_handler = self.get_character_db_handler()
        try:
            delta = int(length)
        except ValueError:
            self.error_log.append({"error_code": 5,
                                   "error_msg": "Not an integer",
                                   "context": "handle_rest",
                                   "timestamp": datetime.now()})
            return False

        try:
            heal = self.compute_rest(quality, delta)
        except ValueError:
            return False

        players = db_handler.increaseEvGroup(heal)
        for a_player in players:
            embed.add_field(
                name= "Soin enregistrée",
                value="Le joueur <@" + a_player['id'] + "> a soigné " + str(int(heal)) + " points de vie.\nIl reste " +
                      a_player['remainingLife'] + " points de vie.",
                inline=False)
        return True

    def handle_walk(self, speed, length, embed):
        character_db_handler = self.get_character_db_handler()
        delta = 0
        try:
            delta = int(length)
        except ValueError:
            self.error_log.append({"error_code": 5,
                                   "error_msg": "Not an integer",
                                   "context": "handle_walk",
                                   "timestamp": datetime.now()})
            return False
        injury = 0
        try:
            injury = self.compute_walk(speed, delta)
        except ValueError:
            return False

        players = character_db_handler.decreaseEvGroup(injury)
        for a_player in players:
            embed.add_field(
                name= "Blessure enregistrée",
                value="Le joueur <@" + a_player['id'] + "> a pris " + str(int(injury)) +
                      " points de dégats.\nIl reste " + a_player['remainingLife'] + " points de vie.",
                inline=False)
        return True

    def get_character_db_handler(self):
        db_handler = CharacterDBHandler()
        return db_handler