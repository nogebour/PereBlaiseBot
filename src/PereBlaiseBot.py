import discord
import random
import re

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

    def check_args(self, message, nb_args, help_message):
        array_args = message.split(" ")
        if len(array_args) < nb_args:
            embed = discord.Embed(color=0xff0000)
            embed.add_field(
                name="Erreur",
                value=help_message,
                inline=True)
            return embed

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

    def get_user_value(self, message):
        array_args = message.split(" ")
        return self.extract_id(array_args[2]), int(array_args[3])

    def get_value(self, message):
        array_args = message.split(" ")
        return int(array_args[2])

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
            operations = comparison[0].split('+')
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
                result, str_display = self.throw_dices(operands, result, str_display)
                str_display = str_display[:-1]
                str_display += ')'
            else:
                ErrorManager().add_error(ErrorCode.NOT_A_POSITIVE_INTEGER, "throw_dices")
        else:
            str_display += operation
            result += int(operation)
        return result, str_display

    def throw_dices(self, operands, result, str_display):
        try:
            occurrence = int(operands[0])
            dice_type = int(operands[1])
        except ValueError:
            ErrorManager().add_error(ErrorCode.NOT_AN_INTEGER, "throw_dices")
            return None, ""
        if occurrence <= 0 or dice_type <= 0:
            ErrorManager().add_error(ErrorCode.NOT_A_POSITIVE_INTEGER, "throw_dices")
            return None, ""
        for x in range(0, occurrence):
            value = random.randint(1, dice_type)
            str_display += (str(value) + '+')
            result += value
        return result, str_display

    def represents_int(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def handle_insults(self, message):
        if "blaise" in message.content.lower() and\
                ("fuck" in message.content.lower() or
                 "encul" in message.content.lower() or
                 "salop" in message.content.lower() or
                 "con" in message.content.lower() or
                 "batard" in message.content.lower() or
                 ("ass" in message.content.lower() and
                  "hole" in message.content.lower())):
            gif = ["https://giphy.com/gifs/gtfo-denzel-washington-shut-the-door-l0HlMSVVw9zqmClLq",
                   "https://giphy.com/gifs/QGzPdYCcBbbZm",
                   "https://giphy.com/gifs/highqualitygifs-s03-e11-cee7A1jKXPDZ6",
                   "https://giphy.com/gifs/rupaulsdragraces5-rupauls-drag-race-rupaul-season-5-26tnoxLPelh9nzzPy",
                   "https://giphy.com/gifs/3d-c4d-cinema-4d-vII0XI8RqUVMY"]
            return True, gif
        elif "blaise" in message.content.lower() and\
                ("pisse" in message.content.lower()):
            gif = ["https://giphy.com/gifs/tisha-campbell-nicole-ari-parker-real-husbands-of-hollywood-cIhprQfD0SDOo"]
            return True, gif
        elif "blaise" in message.content.lower() and\
                ("bite" in message.content.lower() or
                 "dick" in message.content.lower()):
            gif = ["https://giphy.com/gifs/work-adult-safe-XH6dfMa0cLzYA "]
            return True, gif
        elif "blaise" in message.content.lower() and\
                ("whore" in message.content.lower() or
                 "pute" in message.content.lower()):
            gif = ["https://giphy.com/gifs/realitytvgifs-fuck-you-boo-VGNc4ynYaSzy8 "]
            return True, gif
        else:
            return False, []

    def on_message(self, message):
        returned_msgs = []
        result_insult, gif = self.handle_insults(message)
        if result_insult:
            return [DiscordMessage(message.channel, content=gif[random.randint(0, len(gif)-1)])]
        elif message.content.startswith('pereBlaise') or\
                message.content.startswith('PereBlaise') or\
                message.content.startswith('PèreBlaise') or\
                message.content.startswith('pèreBlaise') or\
                message.content.startswith('pB') or\
                message.content.startswith('PB') or\
                message.content.startswith('pb') or\
                message.content.startswith('Pb'):
            args = message.content.split(" ")
            if self.represents_int(args[1]):
                change = int(args[1])
                embed = discord.Embed(color=0x00ff00)
                if change > 0:
                    self.apply_heal(embed, message.author.id, change)
                else:
                    self.apply_injury(embed, message.author.id, (0 - change))
                returned_msgs.append(DiscordMessage(message.channel, embed=embed))

            elif args[1] == 'hi':
                embed = discord.Embed(description="I am pleased to welcome in this area !", color=0x00ff00)
                returned_msgs.append(DiscordMessage(message.channel, embed=embed))
                print(message.channel.id)

            elif args[1] == 'MJblessure':
                embed_result = self.check_args(message.content,
                                               4,
                                               "Syntaxe: '!pereBlaise MJblessure <pseudo> <valeur>'")
                if embed_result is None and message.author.id == MJ_ID:
                    user, value = self.get_user_value(message.content)
                    embed = discord.Embed(color=0x00ff00)
                    self.apply_injury(embed, user, value)
                    returned_msgs.append(DiscordMessage(message.channel, embed=embed))
                else:
                    returned_msgs.append(DiscordMessage(message.channel, embed=embed_result))

            elif args[1] == 'MJsoin':
                embed_result = self.check_args(message.content,
                                               4,
                                               "Syntaxe: '!pereBlaise MJsoin <pseudo> <valeur>'")
                if embed_result is None and message.author.name == "nogebour":
                    user, value = self.get_user_value(message.content)
                    embed = discord.Embed(color=0x00ff00)
                    self.apply_heal(embed, user, value)
                    returned_msgs.append(DiscordMessage(message.channel, embed=embed))
                else:
                    returned_msgs.append(DiscordMessage(message.channel, embed=embed_result))

            elif args[1] == 'blessure':
                embed_result = self.check_args(message.content,
                                               3,
                                               "Syntaxe: '!pereBlaise blessure <valeur>'")
                if embed_result is None:
                    value = self.get_value(message.content)
                    embed = discord.Embed(color=0x00ff00)
                    self.apply_injury(embed, message.author.id, value)
                    returned_msgs.append(DiscordMessage(message.channel, embed=embed))
                else:
                    returned_msgs.append(DiscordMessage(message.channel, embed=embed_result))

            elif args[1] == 'soin' or args[1] == 'soins':
                embed_result = self.check_args(message.content, 3, "Syntaxe: '!pereBlaise soin <valeur>'")
                if embed_result is None:
                    value = self.get_value(message.content)
                    embed = discord.Embed(color=0x00ff00)
                    self.apply_heal(embed, message.author.id, value)
                    returned_msgs.append(DiscordMessage(message.channel, embed=embed))
                else:
                    returned_msgs.append(DiscordMessage(message.channel, embed=embed_result))

            elif args[1] == 'liste' and (args[2] == "armes" or args[2] == "arme"):
                db_handler = CharacterDBHandler()
                db_handler.initialize()
                embeds = db_handler.display_weapons_character(db_handler.import_character(message.author.id))
                for anEmbed in embeds:
                    returned_msgs.append(DiscordMessage(message.channel, embed=anEmbed))

            elif args[1] == 'liste' and args[2] == "stuff":
                db_handler = CharacterDBHandler()
                db_handler.initialize()
                embeds = db_handler.display_stuff_character(db_handler.import_character(message.author.id))
                for anEmbed in embeds:
                    returned_msgs.append(DiscordMessage(message.channel, embed=anEmbed))

            elif args[1] == 'liste' and (args[2] == "skill" or args[2] == "skills"):
                db_handler = CharacterDBHandler()
                db_handler.initialize()
                embeds = db_handler.display_skills_character(db_handler.import_character(message.author.id))
                for anEmbed in embeds:
                    returned_msgs.append(DiscordMessage(message.channel, embed=anEmbed))

            elif args[1] == 'info':
                usr_id = message.author.id
                if len(args) > 2:
                    tmp_usr_id = self.extract_id(args[2])
                    if tmp_usr_id is not None:
                        usr_id = tmp_usr_id
                db_handler = CharacterDBHandler()
                db_handler.initialize()
                embeds = db_handler.display_minimum_info_character(db_handler.import_character(usr_id))
                for anEmbed in embeds:
                    returned_msgs.append(DiscordMessage(message.channel, embed=anEmbed))

            elif args[1] == 'full' and (args[2] == 'info' or args[2] == 'infos'):
                db_handler = CharacterDBHandler()
                db_handler.initialize()
                embeds = db_handler.display_info_character(db_handler.import_character(message.author.id))
                for anEmbed in embeds:
                    returned_msgs.append(DiscordMessage(message.channel, embed=anEmbed))

            elif args[1] == 'bourse' and len(args) == 2:
                db_handler = CharacterDBHandler()
                db_handler.initialize()
                embed = db_handler.display_money_infos(db_handler.import_character(message.author.id))
                returned_msgs.append(DiscordMessage(message.channel, embed=embed))

            elif args[1] == 'bourse':
                embed_result = self.check_args(message.content,
                                               3,
                                               "Syntaxe: '!pereBlaise bourse <or>/<argent>/<bronze>'")
                if embed_result is None:
                    value = self.get_value_str(message.content)
                    db_handler = CharacterDBHandler()
                    db_handler.initialize()
                    gold, silver, bronze = db_handler.money_operation(message.author.id, value)
                    embed_result = discord.Embed(color=0x00ff00)
                    embed_result.add_field(
                        name="Operations comptables enregistrés",
                        value="<@" + MJ_ID + ">: Le joueur <@" + message.author.id + "> a maintenant " +
                              str(gold)+" PO, " +
                              str(silver)+" PA et " +
                              str(bronze)+" PB.",
                        inline=False)
                returned_msgs.append(DiscordMessage(message.channel, embed=embed_result))

            elif args[1] == 'MJbourse':
                embed_result = self.check_args(message.content,
                                               4,
                                               "Syntaxe: '!pereBlaise MJbourse <user> <or>/<argent>/<bronze>'")
                if embed_result is None:
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

            elif args[1] == "temps" and len(args) == 2:
                settings = SettingsHandler()
                settings.initialize()
                embed = discord.Embed(color=0x00ff00)
                embed.add_field(
                    name="Heure du jeu",
                    value="<@"+message.author.id+"> a demandé la date et on est le " +
                          settings.current_time.strftime("%d/%m/%Y") +
                          " à " +
                          settings.current_time.strftime("%H:%M")+".",
                    inline=False)
                returned_msgs.append(DiscordMessage(message.channel, embed=embed))

            elif args[1] == "temps" and args[2] == "passe" and len(args) == 3:
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

            elif args[1] == "temps" and len(args) == 3:
                settings = SettingsHandler()
                settings.initialize()
                embed = discord.Embed(color=0x00ff00)
                if self.make_time_operation(args[2], message, settings, embed):
                    settings.save_settings()
                returned_msgs.append(DiscordMessage(message.channel, embed=embed))

            elif args[1] == "temps" and len(args) == 5:
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
            elif args[1] == "save":
                if message.author.id == MJ_ID:
                    db_handler = DbHandler()
                    db_handler.retrieve_game()
                    db_handler.save_snapshot_game()
            elif args[1].lower() == "roll" and len(args) > 2:
                returned_msgs.append(DiscordMessage(message.channel,
                                                    content=("<@"+message.author.id+">\n" +
                                                             self.roll(''.join(args[2:])))))
            else:
                returned_msgs.append(DiscordMessage(message.channel,
                                                    content=("Hello jeune aventurier!\n"
                                                             "Je ne te comprends pas."
                                                             " Va donc voir le channel <#"+HELP_CHANNEL+">")))
        return returned_msgs
