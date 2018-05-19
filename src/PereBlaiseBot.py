import discord
import random
import re
import unidecode

from .CharacterDBHandler import CharacterDBHandler
from .Settings import SettingsHandler
from .Database.DbHandler import DbHandler
from .Error.ErrorManager import ErrorManager, ErrorCode

HELP_CHANNEL = '387149097037070346'
MJ_CHANNEL = '411248354534752256'
MJ_ID = '294164488427405312'


class DiscordMessage:
    discord_channel = None
    str_msg = None
    embed_msg = None

    def __init__(self, discord_channel, content=None, embed=None):
        self.discord_channel = discord_channel
        self.str_msg = content
        self.embed_msg = embed


class PereBlaiseBot:
    def __init__(self):
        self.character_db_handler = CharacterDBHandler()

    def check_args(self, message, nb_args, syntax_msg):
        array_args = message.split(" ")
        if len(array_args) < nb_args:
            ErrorManager().add_error(ErrorCode.INVALID_SYNTAX, "check_args", [syntax_msg])

    def get_user(self, args, message, index_user):
        user_id = None
        if len(args) >= (index_user + 1):
            user_id = self.extract_id(args[index_user])
        if user_id is None:
            user_id = message.author.id
        return user_id

    def extract_id(self, args):
        user_id = None
        if args.startswith("<@!"):
            user_id = args[3:-1]
        elif args.startswith("<@"):
            user_id = args[2:-1]
        return user_id

    def get_user_value(self, message, user_idx=2, value_idx=3):
        array_args = message.split(" ")
        return self.extract_id(array_args[user_idx]), int(array_args[value_idx])

    def get_value(self, message, idx=2):
        array_args = message.split(" ")
        return int(array_args[idx])

    def get_user_value_str(self, message):
        array_args = message.split(" ")
        return self.extract_id(array_args[2]), array_args[3]

    def get_value_str(self, message):
        array_args = message.split(" ")
        return array_args[2]

    def make_time_operation(self, delta_min, message, settings, embed):
        result = False
        if message.author.id != MJ_ID:
            ErrorManager().add_error(ErrorCode.GM_COMMAND_ONLY, "make_time_operation")
            return result
        delta = 0
        try:
            delta = int(delta_min)
        except ValueError:
            ErrorManager().add_error(ErrorCode.NOT_AN_INTEGER, "make_time_operation")
            return result
        if delta <= 0:
            ErrorManager().add_error(ErrorCode.NOT_A_POSITIVE_INTEGER, "make_time_operation")
            return result
        current_time = settings.add_time(delta)
        result = True
        embed.add_field(
            name="Temps ajouté",
            value="<@" + message.author.id + "> a demandé l'ajout de " + delta_min +
                  " minutes.\nNous sommes donc maintenant le " +
                  current_time.strftime("%d/%m/%Y") + " à " + current_time.strftime("%H:%M") + ".",
            inline=False)
        return result

    def apply_heal(self, embed, user, value):
        self.character_db_handler.initialize()
        remaining_life = self.character_db_handler.increase_ev(user, value)
        embed.add_field(
            name="Soin enregistré",
            value="Le joueur <@" + user + "> a soigné " + str(
                value) + " points de vie.\nIl reste " + remaining_life + " points de vie.",
            inline=False)

    def apply_injury(self, embed, user, value):
        self.character_db_handler.initialize()
        remaining_life = self.character_db_handler.decrease_ev(user, value)
        embed.add_field(
            name="Blessure enregistrée",
            value="Le joueur <@" + user + "> a reçu " + str(
                value) + " points de dégats.\nIl reste " + remaining_life + " points de vie.",
            inline=False)

    def roll(self, dice_cmd):
        final_result = ''
        commands = dice_cmd.replace(' ', '').split('&')
        for command in commands:
            result = 0
            comparison = command.split('<')
            threshold = None
            if len(comparison) > 1:
                threshold = int(comparison[1])
            operations = re.split('[+,-]', comparison[0])
            str_display = comparison[0] + '='
            for operation in operations:
                result, str_display = self.compute_and_display_single_operation(operation, result, str_display)
                str_display += '+'
            str_display = str_display[:-1]
            str_display += ('='+str(result))
            str_display = self.display_result_status(result, str_display, threshold)
            final_result += str_display+'\n'
        return final_result[:-1]

    def display_result_status(self, result, str_display, threshold):
        if threshold is not None:
            str_display += ('<' + str(threshold))
            if result < threshold:
                str_display += ' --> Reussite'
            else:
                str_display += ' --> Echec'
        return str_display

    def compute_and_display_single_operation(self, operation, result, str_display):
        if ('D' in operation) or ('d' in operation):
            operands = re.split('[D,d]', operation)
            if len(operands) == 2:
                str_display += '('
                result, str_display = self.throw_dices(operands[0], operands[1], result, str_display)
                if result is not None:
                    str_display = str_display[:-1]
                    str_display += ')'
            else:
                ErrorManager().add_error(ErrorCode.INVALID_SYNTAX, "compute_and_display_single_operation", ["[0-9]*[d,D][0-9]*"])
                return None, ""
        else:
            try:
                str_display += operation
                result += int(operation)
            except ValueError:
                ErrorManager().add_error(ErrorCode.NOT_AN_INTEGER, "throw_dices")
                return None, ""
        return result, str_display

    def throw_dices(self, occurrence, dice_type, result, str_display):
        try:
            occurrence = int(occurrence)
            dice_type = int(dice_type)
        except ValueError:
            ErrorManager().add_error(ErrorCode.NOT_AN_INTEGER, "throw_dices")
            return None, ""
        if occurrence <= 0 or dice_type <= 0:
            ErrorManager().add_error(ErrorCode.NOT_A_POSITIVE_INTEGER, "throw_dices")
            return None, ""

        for x in range(0, occurrence):
            value = random.randint(1, dice_type)
            str_display += (str(value) + '+')
            result = None if result is None else (result + value)
        return result, str_display

    def represents_int(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def handle_insults(self, message):
        lowered_msg = unidecode.unidecode(message.lower())
        if "blaise" in lowered_msg and\
                ("fuck" in lowered_msg or
                 "encul" in lowered_msg or
                 "salop" in lowered_msg or
                 "con" in lowered_msg or
                 "batard" in lowered_msg or
                 ("ass" in lowered_msg and
                  "hole" in lowered_msg)):
            gif = ["https://giphy.com/gifs/gtfo-denzel-washington-shut-the-door-l0HlMSVVw9zqmClLq",
                   "https://giphy.com/gifs/QGzPdYCcBbbZm",
                   "https://giphy.com/gifs/highqualitygifs-s03-e11-cee7A1jKXPDZ6",
                   "https://giphy.com/gifs/rupaulsdragraces5-rupauls-drag-race-rupaul-season-5-26tnoxLPelh9nzzPy",
                   "https://giphy.com/gifs/3d-c4d-cinema-4d-vII0XI8RqUVMY"]
            return True, gif
        elif "blaise" in lowered_msg and\
                ("pisse" in lowered_msg):
            gif = ["https://giphy.com/gifs/tisha-campbell-nicole-ari-parker-real-husbands-of-hollywood-cIhprQfD0SDOo"]
            return True, gif
        elif "blaise" in lowered_msg and\
                ("bite" in lowered_msg or
                 "dick" in lowered_msg):
            gif = ["https://giphy.com/gifs/work-adult-safe-XH6dfMa0cLzYA "]
            return True, gif
        elif "blaise" in lowered_msg and\
                ("whore" in lowered_msg or
                 "pute" in lowered_msg):
            gif = ["https://giphy.com/gifs/realitytvgifs-fuck-you-boo-VGNc4ynYaSzy8 "]
            return True, gif
        else:
            return False, []

    def detect_command_keyword(self, message):
        message = unidecode.unidecode(message).lower()
        return message.startswith('pereblaise') or \
            message.startswith('pb')

    def handle_life_operations(self, parsed_command, message, returned_msgs):
        if self.represents_int(parsed_command[0]):
            change = int(parsed_command[0])
            embed = discord.Embed(color=0x00ff00)
            if change > 0:
                self.apply_heal(embed, message.author.id, change)
            else:
                self.apply_injury(embed, message.author.id, (0 - change))
            returned_msgs.append(DiscordMessage(message.channel, embed=embed))

    def handle_welcome(self, args, message, returned_msgs):
        if unidecode.unidecode(args[0]) == 'hi':
            embed = discord.Embed(description="I am pleased to welcome in this area !", color=0x00ff00)
            returned_msgs.append(DiscordMessage(message.channel, embed=embed))

    def display_error(self, returned_msg, channel):
        for an_error in ErrorManager.error_log:
            embed = discord.Embed(color=0xff0000)
            embed.add_field(
                name="Erreur",
                value=an_error,
                inline=True)
            returned_msg.append(DiscordMessage(channel, embed=embed))

    def handle_gm_injury(self, args, message, returned_msgs):
        syntax_msg = "!pereBlaise MJblessure <pseudo> <valeur>"
        #Decoding
        if args[0] == 'MJblessure':
            embed = None
            self.check_args(message.content, 4, syntax_msg)

        #Check
            if message.author.id == MJ_ID:
                user, value = self.get_user_value(message.content, 2, 3)
                print(str(user)+" "+str(value))
                embed = discord.Embed(color=0x00ff00)
                self.apply_injury(embed, user, value)
            else:
                ErrorManager().add_error(ErrorCode.GM_COMMAND_ONLY,
                                         "handle_gm_injury")

        #display
            if len(ErrorManager.error_log) > 0:
                self.display_error(returned_msgs, message.channel)
            if embed is not None:
                returned_msgs.append(DiscordMessage(message.channel, embed=embed))

    def handle_gm_heal(self, args, message, returned_msgs):
        syntax_msg = "pereBlaise MJsoin <pseudo> <valeur>"
        if args[0] == 'MJsoin':
            embed = None
            self.check_args(message.content, 4, syntax_msg)
            if message.author.id == MJ_ID:
                user, value = self.get_user_value(message.content, 2, 3)
                embed = discord.Embed(color=0x00ff00)
                self.apply_heal(embed, user, value)

            if len(ErrorManager.error_log) > 0:
                self.display_error(returned_msgs, message.channel)
            if embed is not None:
                returned_msgs.append(DiscordMessage(message.channel, embed=embed))

    def handle_injury(self, args, message, returned_msgs):
        syntax_msg = "pereBlaise blessure <valeur>"
        if args[0] == 'blessure':
            self.check_args(message.content, 3, syntax_msg)

            value = self.get_value(message.content, 1)
            embed = discord.Embed(color=0x00ff00)
            self.apply_injury(embed, message.author.id, value)
            returned_msgs.append(DiscordMessage(message.channel, embed=embed))
            if len(ErrorManager.error_log) > 0:
                self.display_error(returned_msgs, message.channel)
            if embed is not None:
                returned_msgs.append(DiscordMessage(message.channel, embed=embed))

    def handle_heal(self, args, message, returned_msgs):
        if args[0] == 'soin' or args[0] == 'soins':
            syntax_msg = "pereBlaise soin <valeur>"
            self.check_args(message.content, 2, syntax_msg)
            value = self.get_value(message.content, 1)
            embed = discord.Embed(color=0x00ff00)
            self.apply_heal(embed, message.author.id, value)

            if len(ErrorManager.error_log) > 0:
                self.display_error(returned_msgs, message.channel)
            if embed is not None:
                returned_msgs.append(DiscordMessage(message.channel, embed=embed))

    def on_message(self, message):
        returned_msgs = []
        result_insult, gif = self.handle_insults(message.content)
        if result_insult:
            return [DiscordMessage(message.channel, content=gif[random.randint(0, len(gif)-1)])]
        elif self.detect_command_keyword(message.content):
            args = message.content.split(" ")
            self.handle_life_operations(args.pop(0), message, returned_msgs)
            self.handle_welcome(args.pop(0), message, returned_msgs)
            self.handle_gm_injury(args.pop(0), message, returned_msgs)
            self.handle_gm_heal(args.pop(0), message, returned_msgs)
            self.handle_injury(args.pop(0), message, returned_msgs)
            self.handle_list_weapons(args, message, returned_msgs)
            self.handle_list_stuff(args, message, returned_msgs)
            self.handle_list_skills(args, message, returned_msgs)
            self.handle_info(args, message, returned_msgs)
            self.handle_full_info(args, message, returned_msgs)
            self.handle_money(args, message, returned_msgs)
            self.handle_money_operation(args, message, returned_msgs)
            self.handle_money_operation_gm(args, message, returned_msgs)
            self.handle_time(args, message, returned_msgs)
            self.handle_time_start_game(args, message, returned_msgs)
            self.handle_time_operation(args, message, returned_msgs)
            self.handle_time_walk_rest(args, message, returned_msgs)
            self.handle_save(args, message)
            self.handle_roll(args, message, returned_msgs)

#                returned_msgs.append(DiscordMessage(message.channel,
#                                                    content=("Hello jeune aventurier!\n"
#                                                             "Je ne te comprends pas."
#                                                             " Va donc voir le channel <#"+HELP_CHANNEL+">")))
        ErrorManager().clear_error()
        return returned_msgs

    def handle_roll(self, args, message, returned_msgs):
        if args[1].lower() == "roll" and len(args) > 2:
            returned_msgs.append(DiscordMessage(message.channel,
                                                content=("<@" + message.author.id + ">\n" +
                                                         self.roll(''.join(args[2:])))))

    def handle_save(self, args, message):
        if args[1] == "save":
            if message.author.id == MJ_ID:
                db_handler = DbHandler()
                db_handler.retrieve_game()
                db_handler.save_snapshot_game()

    def handle_time_walk_rest(self, args, message, returned_msgs):
        if args[1] == "temps" and len(args) == 5:
            if args[2] == "repos" or args[2] == "marche":
                settings = SettingsHandler()
                settings.initialize()
                embed = discord.Embed(color=0x00ff00)
                if self.make_time_operation(args[4], message, settings, embed):
                    if args[2] == 'repos':
                        print("repos")
                        settings.handle_rest(args[3], args[4], embed)
                    elif args[2] == 'marche':
                        print("Marche")
                        settings.handle_walk(args[3], args[4], embed)
                returned_msgs.append(DiscordMessage(message.channel, embed=embed))

    def handle_time_operation(self, args, message, returned_msgs):
        if args[1] == "temps" and len(args) == 3:
            settings = SettingsHandler()
            settings.initialize()
            embed = discord.Embed(color=0x00ff00)
            if self.make_time_operation(args[2], message, settings, embed):
                settings.save_settings()
            returned_msgs.append(DiscordMessage(message.channel, embed=embed))

    def handle_time_start_game(self, args, message, returned_msgs):
        if args[1] == "temps" and args[2] == "passe" and len(args) == 3:
            settings = SettingsHandler()
            settings.initialize()
            delta = settings.get_elapsed_time()
            embed = discord.Embed(color=0x00ff00)
            embed.add_field(
                name="Durée de l'aventure",
                value=("Pour information l'aventure à commencé depuis " +
                       str(delta)).replace("day", "jour"),
                inline=False)
            returned_msgs.append(DiscordMessage(message.channel, embed=embed))

    def handle_time(self, args, message, returned_msgs):
        if args[1] == "temps" and len(args) == 2:
            settings = SettingsHandler()
            settings.initialize()
            embed = discord.Embed(color=0x00ff00)
            embed.add_field(
                name="Heure du jeu",
                value="<@" + message.author.id + "> a demandé la date et on est le " +
                      settings.current_time.strftime("%d/%m/%Y") +
                      " à " +
                      settings.current_time.strftime("%H:%M") + ".",
                inline=False)
            returned_msgs.append(DiscordMessage(message.channel, embed=embed))

    def handle_money_operation_gm(self, args, message, returned_msgs):
        if args[1] == 'MJbourse':
            syntax_msg = "pereBlaise MJbourse <user> <or>/<argent>/<bronze>"
            self.check_args(message.content, 4, syntax_msg)
            user, value = self.get_user_value_str(message.content)
            db_handler = CharacterDBHandler()
            db_handler.initialize()
            gold, silver, bronze = db_handler.money_operation(user, value)
            embed_result = discord.Embed(color=0x00ff00)
            embed_result.add_field(
                name="Operations comptables enregistrés",
                value="<@" + MJ_ID + ">: Le joueur <@" + user + "> a maintenant " + str(gold) +
                      " PO, " + str(silver) + " PA et " + str(bronze) + " PB.",
                inline=False)
            returned_msgs.append(DiscordMessage(message.channel, embed=embed_result))

    def handle_money_operation(self, args, message, returned_msgs):
        if args[1] == 'bourse':
            syntax_msg = "pereBlaise bourse <or>/<argent>/<bronze>"
            self.check_args(message.content, 3, syntax_msg)
            value = self.get_value_str(message.content)
            db_handler = CharacterDBHandler()
            db_handler.initialize()
            gold, silver, bronze = db_handler.money_operation(message.author.id, value)
            embed_result = discord.Embed(color=0x00ff00)
            embed_result.add_field(
                name="Operations comptables enregistrés",
                value="<@" + MJ_ID + ">: Le joueur <@" + message.author.id + "> a maintenant " +
                      str(gold) + " PO, " +
                      str(silver) + " PA et " +
                      str(bronze) + " PB.",
                inline=False)
            returned_msgs.append(DiscordMessage(message.channel, embed=embed_result))

    def handle_money(self, args, message, returned_msgs):
        if args[1] == 'bourse' and len(args) == 2:
            db_handler = CharacterDBHandler()
            db_handler.initialize()
            embed = db_handler.display_money_infos(db_handler.import_character(message.author.id))
            returned_msgs.append(DiscordMessage(message.channel, embed=embed))

    def handle_full_info(self, args, message, returned_msgs):
        if args[1] == 'full' and (args[2] == 'info' or args[2] == 'infos'):
            db_handler = CharacterDBHandler()
            db_handler.initialize()
            embeds = db_handler.display_info_character(db_handler.import_character(message.author.id))
            for an_embed in embeds:
                returned_msgs.append(DiscordMessage(message.channel, embed=an_embed))

    def handle_info(self, args, message, returned_msgs):
        if args[1] == 'info':
            usr_id = message.author.id
            if len(args) > 2:
                tmp_usr_id = self.extract_id(args[2])
                if tmp_usr_id is not None:
                    usr_id = tmp_usr_id
            db_handler = CharacterDBHandler()
            db_handler.initialize()
            embeds = db_handler.display_minimum_info_character(db_handler.import_character(usr_id))
            for an_embed in embeds:
                returned_msgs.append(DiscordMessage(message.channel, embed=an_embed))

    def handle_list_skills(self, args, message, returned_msgs):
        if args[1] == 'liste' and (args[2] == "skill" or args[2] == "skills"):
            db_handler = CharacterDBHandler()
            db_handler.initialize()
            embeds = db_handler.display_skills_character(db_handler.import_character(message.author.id))
            for an_embed in embeds:
                returned_msgs.append(DiscordMessage(message.channel, embed=an_embed))

    def handle_list_stuff(self, args, message, returned_msgs):
        if args[1] == 'liste' and args[2] == "stuff":
            db_handler = CharacterDBHandler()
            db_handler.initialize()
            embeds = db_handler.display_stuff_character(db_handler.import_character(message.author.id))
            for an_embed in embeds:
                returned_msgs.append(DiscordMessage(message.channel, embed=an_embed))

    def handle_list_weapons(self, args, message, returned_msgs):
        if args[1] == 'liste' and (args[2] == "armes" or args[2] == "arme"):
            db_handler = CharacterDBHandler()
            db_handler.initialize()
            embeds = db_handler.display_weapons_character(db_handler.import_character(message.author.id))
            for an_embed in embeds:
                returned_msgs.append(DiscordMessage(message.channel, embed=an_embed))
