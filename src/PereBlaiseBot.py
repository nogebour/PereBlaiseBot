# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import random
import re

import discord
from CharacterDBHandler import CharacterDBHandler
from Settings import SettingsHandler

from src.DbHandler import DbHandler

HELP_CHANNEL = '387149097037070346'
MJ_CHANNEL = '386082775066869760'
MJ_ID = '294164488427405312'

class DiscordMessage:
    discordChannel = None
    strMessage = None
    embedMessage = None

    def __init__(self, iDiscordChannel, content = None, embed = None):
        self.discordChannel = iDiscordChannel
        self.strMessage = content
        self.embedMessage = embed

class PereBlaiseBot:
    def checkArgs(self, message, nbArgs, help):
        arrayArgs = message.split(" ")
        if(len(arrayArgs) < nbArgs):
            embed = discord.Embed(color=0xff0000)
            embed.add_field(
                name="Erreur",
                value=help,
                inline=True)
            return embed

    def getUser(self, args, message, indexUser):
        userId = None
        if len(args) >= (indexUser+1):
            userId = self.extractId(args[indexUser])
        if userId is None:
            userId = message.author.id
        return userId


    def extractId(self, args):
        userId = None
        if args.startswith("<@!"):
            userId = args[3:-1]
        elif args.startswith("<@"):
            userId = args[2:-1]
        return userId

    def getUserValue(self, message):
        arrayArgs = message.split(" ")
        return self.extractId(arrayArgs[2]), int(arrayArgs[3])

    def getValue(self, message):
        arrayArgs = message.split(" ")
        return int(arrayArgs[2])

    def getUserValueStr(self, message):
        arrayArgs = message.split(" ")
        return self.extractId(arrayArgs[2]), arrayArgs[3]

    def getValueStr(self, message):
        arrayArgs = message.split(" ")
        return arrayArgs[2]

    def makeTimeOperation(self, deltaMinutes, message, theSettings, embed):
        result = False
        if (message.author.id == MJ_ID):
            delta = 0
            try:
                delta = int(deltaMinutes)
            except ValueError:
                print("Not an integer")
                return
            if delta > 0:
                currentTime = theSettings.add_time(delta)
                result = True
                embed.add_field(
                    name=("Temps ajouté"),
                    value="<@" + message.author.id + "> a demandé l'ajout de " + deltaMinutes + " minutes.\nNous sommes donc maintenant le " + currentTime.strftime("%d/%m/%Y") + " à " + currentTime.strftime("%H:%M") + ".",
                    inline=False)
        return result

    def applyHeal(self, embed, user, value):
        testDb = CharacterDBHandler()
        remainingLife = testDb.increaseEv(user,value)
        embed.add_field(
            name=("Soin enregistrée"),
            value="Le joueur <@" + user + "> a soigné " + str(
                value) + " points de vie.\nIl reste " + remainingLife + " points de vie.",
            inline=False)


    def applyInjury(self, embed, user, value):
        testDb = CharacterDBHandler()
        remainingLife = testDb.decreaseEv(user,value)
        embed.add_field(
            name=("Blessure enregistrée"),
            value="Le joueur <@" + user + "> a recu " + str(
                value) + " points de dégats.\nIl reste " + remainingLife + " points de vie.",
            inline=False)

    def roll(self, diceCommand):
        finalResult = ''
        commands = diceCommand.replace(' ','').split('&')
        for command in commands:
            result = 0
            comparison = command.split('<')
            threshold = None
            if(len(comparison) > 1):
                threshold = int(comparison[1])
            operations = comparison[0].split('+')
            strDisplay = comparison[0] + '='
            for operation in operations:
                if ('D' in operation) or ('d' in operation):
                    operands = re.split('D|d',operation)
                    if(len(operands) == 2):
                        strDisplay += '('
                        occurence = int(operands[0])
                        diceType = int(operands[1])
                        for x in range(0, occurence):
                            value = random.randint(1, diceType)
                            strDisplay += (str(value) + '+')
                            result += value
                        strDisplay = strDisplay[:-1]
                        strDisplay += ')'
                else:
                    strDisplay += operation
                    result += int(operation)
                strDisplay += '+'
            strDisplay = strDisplay[:-1]
            strDisplay += ('='+str(result))
            if(threshold is not None):
                strDisplay += ('<'+str(threshold))
                if(result < threshold):
                    strDisplay += ' --> Reussite'
                else:
                    strDisplay += ' --> Echec'
            finalResult += strDisplay+'\n'
        return finalResult[:-1]

    def representsInt(self,s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def handleInsults(self, message):
        if "blaise" in message.content.lower() and ("fuck" in message.content.lower() or "encul" in message.content.lower() or "salop" in message.content.lower() or "con" in message.content.lower() or "batard" in message.content.lower() or ("ass" in message.content.lower() and "hole" in message.content.lower())):
            gif = ["https://giphy.com/gifs/gtfo-denzel-washington-shut-the-door-l0HlMSVVw9zqmClLq", "https://giphy.com/gifs/QGzPdYCcBbbZm", "https://giphy.com/gifs/highqualitygifs-s03-e11-cee7A1jKXPDZ6", "https://giphy.com/gifs/rupaulsdragraces5-rupauls-drag-race-rupaul-season-5-26tnoxLPelh9nzzPy", "https://giphy.com/gifs/3d-c4d-cinema-4d-vII0XI8RqUVMY"]
            return True, gif
        elif "blaise" in message.content.lower() and ("pisse" in message.content.lower()):
            gif = ["https://giphy.com/gifs/tisha-campbell-nicole-ari-parker-real-husbands-of-hollywood-cIhprQfD0SDOo"]
            return True, gif
        elif "blaise" in message.content.lower() and ("bite" in message.content.lower() or "dick" in message.content.lower()):
            gif = ["https://giphy.com/gifs/work-adult-safe-XH6dfMa0cLzYA "]
            return True, gif
        elif "blaise" in message.content.lower() and ("whore" in message.content.lower() or "pute" in message.content.lower()):
            gif = ["https://giphy.com/gifs/realitytvgifs-fuck-you-boo-VGNc4ynYaSzy8 "]
            return True, gif
        else:
            return False, []

    def on_message(self, message, client):
        returnedMessage = []
        resultInsult, gif = self.handleInsults(message)
        if resultInsult:
            return [DiscordMessage(message.channel, content=gif[random.randint(0, len(gif)-1)])]
        elif message.content.startswith('pereBlaise') or message.content.startswith('PereBlaise') or message.content.startswith('PèreBlaise') or message.content.startswith('pèreBlaise') or message.content.startswith('pB') or message.content.startswith('PB') or message.content.startswith('pb') or message.content.startswith('Pb'):
            args = message.content.split(" ")
            if self.representsInt(args[1]):
                change = int(args[1])
                embed = discord.Embed(color=0x00ff00)
                if change > 0:
                    self.applyHeal(embed, message.author.id, change)
                else:
                    self.applyInjury(embed, message.author.id, (0-change))
                returnedMessage.append(DiscordMessage(message.channel, embed=embed))

            elif args[1] == 'hi':
                embed = discord.Embed(description="I am pleased to welcome in this area !", color=0x00ff00)
                returnedMessage.append(DiscordMessage(message.channel, embed=embed))
                print(message.channel.id)

            elif args[1] == 'MJblessure':
                embedResult = self.checkArgs(message.content, 4, "Syntaxe: '!pereBlaise MJblessure <pseudo> <valeur>'")
                if embedResult is None and message.author.id==MJ_ID:
                    user, value = self.getUserValue(message.content)
                    embed = discord.Embed(color=0x00ff00)
                    self.applyInjury(embed, user, value)
                    returnedMessage.append(DiscordMessage(message.channel, embed=embed))
                else:
                    returnedMessage.append(DiscordMessage(message.channel, embed=embedResult))

            elif args[1] == 'MJsoin':
                embedResult = self.checkArgs(message.content, 4, "Syntaxe: '!pereBlaise MJsoin <pseudo> <valeur>'")
                if embedResult is None and message.author.name=="nogebour":
                    user, value = self.getUserValue(message.content)
                    embed = discord.Embed(color=0x00ff00)
                    self.applyHeal(embed, user, value)
                    returnedMessage.append(DiscordMessage(message.channel, embed=embed))
                else:
                    returnedMessage.append(DiscordMessage(message.channel, embed=embedResult))

            elif args[1] == 'blessure':
                embedResult = self.checkArgs(message.content, 3, "Syntaxe: '!pereBlaise blessure <valeur>'")
                if embedResult is None:
                    value = self.getValue(message.content)
                    embed = discord.Embed(color=0x00ff00)
                    self.applyInjury(embed, message.author.id, value)
                    returnedMessage.append(DiscordMessage(message.channel, embed=embed))
                else:
                    returnedMessage.append(DiscordMessage(message.channel, embed=embedResult))

            elif args[1] == 'soin' or args[1] == 'soins':
                embedResult = self.checkArgs(message.content, 3, "Syntaxe: '!pereBlaise soin <valeur>'")
                if embedResult is None:
                    value = self.getValue(message.content)
                    embed = discord.Embed(color=0x00ff00)
                    self.applyHeal(embed, message.author.id, value)
                    returnedMessage.append(DiscordMessage(message.channel, embed=embed))
                else:
                    returnedMessage.append(DiscordMessage(message.channel, embed=embedResult))

            elif args[1] == 'liste' and (args[2] == "armes" or args[2] == "arme"):
                testDb = CharacterDBHandler()
                embeds = testDb.displayWeaponsCharacter(testDb.importCharacter(message.author.id))
                for anEmbed in embeds:
                    returnedMessage.append(DiscordMessage(message.channel, embed=anEmbed))

            elif args[1] == 'liste' and args[2] == "stuff":
                testDb = CharacterDBHandler()
                embeds = testDb.displayStuffCharacter(testDb.importCharacter(message.author.id))
                for anEmbed in embeds:
                    returnedMessage.append(DiscordMessage(message.channel, embed=anEmbed))

            elif args[1] == 'liste' and (args[2] == "skill" or args[2] == "skills"):
                testDb = CharacterDBHandler()
                embeds = testDb.displaySkillsCharacter(testDb.importCharacter(message.author.id))
                for anEmbed in embeds:
                    returnedMessage.append(DiscordMessage(message.channel, embed=anEmbed))

            elif args[1] == 'info':
                userId = message.author.id
                if len(args) > 2:
                    tmpUserId = self.extractId(args[2])
                    if tmpUserId is not None:
                        userId = tmpUserId
                testDb = CharacterDBHandler()
                embeds = testDb.displayMinimumInfoCharacter(testDb.importCharacter(userId))
                for anEmbed in embeds:
                    returnedMessage.append(DiscordMessage(message.channel, embed=anEmbed))

            elif args[1] == 'full' and (args[2] == 'info' or args[2] == 'infos'):
                testDb = CharacterDBHandler()
                embeds = testDb.displayInfoCharacter(testDb.importCharacter(message.author.id))
                for anEmbed in embeds:
                    returnedMessage.append(DiscordMessage(message.channel, embed=anEmbed))

            elif args[1] == 'bourse' and len(args) == 2:
                testDb = CharacterDBHandler()
                embed = testDb.displayMoneyInfos(testDb.importCharacter(message.author.id))
                returnedMessage.append(DiscordMessage(message.channel, embed=embed))

            elif args[1] == 'bourse':
                embedResult = self.checkArgs(message.content, 3, "Syntaxe: '!pereBlaise bourse <or>/<argent>/<bronze>'")
                if embedResult is None:
                    value = self.getValueStr(message.content)
                    testDb = CharacterDBHandler()
                    gold, silver, bronze = testDb.moneyOperation(message.author.id, value)
                    embedResult = discord.Embed(color=0x00ff00)
                    embedResult.add_field(
                        name=("Operations comptables enregistrés"),
                        value="Le joueur "+message.author.name+" a "+str(gold)+" PO, "+str(silver)+" PA et "+str(bronze)+" PB.",
                        inline=False)
                    returnedMessage.append(DiscordMessage(client.get_channel(MJ_CHANNEL), embed=embedResult, content="<@"+MJ_ID+">"))
                returnedMessage.append(DiscordMessage(message.channel, embed=embedResult))

            elif args[1] == 'MJbourse':
                embedResult = self.checkArgs(message.content, 4, "Syntaxe: '!pereBlaise MJbourse <user> <or>/<argent>/<bronze>'")
                if embedResult is None:
                    user, value = self.getUserValueStr(message.content)
                    testDb = CharacterDBHandler()
                    gold, silver, bronze = testDb.moneyOperation(user, value)
                    embedResult = discord.Embed(color=0x00ff00)
                    embedResult.add_field(
                        name=("Operations comptables enregistrés"),
                        value="Le joueur <@"+user+"> a "+str(gold)+" PO, "+str(silver)+" PA et "+str(bronze)+" PB.",
                        inline=False)
                    returnedMessage.append(DiscordMessage(client.get_channel(MJ_CHANNEL), embed=embedResult, content="<@"+MJ_ID+">"))
                returnedMessage.append(DiscordMessage(message.channel, embed=embedResult))

            elif args[1] == "temps" and len(args) == 2:
                theSettings = SettingsHandler()
                embed = discord.Embed(color=0x00ff00)
                embed.add_field(
                    name=("Heure du jeu"),
                    value="<@"+message.author.id+"> a demandé la date et on est le "+theSettings.current_time.strftime("%d/%m/%Y")+" à "+theSettings.current_time.strftime("%H:%M")+".",
                    inline=False)
                returnedMessage.append(DiscordMessage(message.channel, embed=embed))

            elif args[1] == "temps" and args[2] == "passe" and len(args) == 3:
                theSettings = SettingsHandler()
                aDelta = theSettings.get_elapsed_time()
                embed = discord.Embed(color=0x00ff00)
                embed.add_field(
                    name=("Durée de l'aventure"),
                    value=("Pour information l'aventure à commencé depuis "+str(aDelta)).replace("day", "jour"),
                    inline=False)
                returnedMessage.append(DiscordMessage(message.channel, embed=embed))

            elif args[1] == "temps" and len(args) == 3:
                theSettings = SettingsHandler()
                embed = discord.Embed(color=0x00ff00)
                if(self.makeTimeOperation(args[2], message, theSettings, embed)):
                    theSettings.save_settings()
                returnedMessage.append(DiscordMessage(message.channel, embed=embed))

            elif args[1] == "temps" and len(args) == 5:
                if(args[2] == "repos" or args[2] == "marche"):
                    theSettings = SettingsHandler()
                    embed = discord.Embed(color=0x00ff00)
                    if self.makeTimeOperation(args[4], message, theSettings, embed):
                        if args[2] == 'repos':
                            print("repos")
                            theSettings.handle_rest(args[3], args[4], embed)
                        elif args[2] == 'marche':
                            print("Marche")
                            theSettings.handle_walk(args[3], args[4], embed)
                    returnedMessage.append(DiscordMessage(message.channel, embed=embed))
            elif args[1] == "save":
                if message.author.id == MJ_ID:
                    aDbHandler = DbHandler()
                    aDbHandler.retrieve_game()
                    aDbHandler.save_snapshot_game()
            elif args[1].lower() == "roll" and len(args) > 2:
                returnedMessage.append(DiscordMessage(message.channel, content=("<@"+message.author.id+">\n"+self.roll(''.join(args[2:])))))
            else:
                returnedMessage.append(DiscordMessage(message.channel, content=("Hello jeune aventurier!\nJe ne te comprends pas. Va donc voir le channel <#"+HELP_CHANNEL+">")))
        return returnedMessage