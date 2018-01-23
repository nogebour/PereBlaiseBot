# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
from discord.ext.commands import Bot
import random
import platform
import re
from CharacterDBHandler import CharacterDBHandler
from DbHandler import DbHandler
from Settings import SettingsHandler

# Here you can modify the bot's prefix and description and wether it sends help in direct messages or not.
client = Bot(description="Basic Bot by Habchy#1665", command_prefix="/Blaise:", pm_help = True)

HELP_CHANNEL = '387149097037070346'
MJ_CHANNEL = '386082775066869760'
MJ_ID = '294164488427405312'


# This is what happens everytime the bot launches. In this case, it prints information like server count, user count the bot is connected to, and the bot id in the console.
# Do not mess with it because the bot can break, if you wish to do so, please consult me or someone trusted.
@client.event
async def on_ready():
	print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
	print('--------')
	print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
	print('--------')
	print('Use this link to invite {}:'.format(client.user.name))
	print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
	print('--------')
	print('Support Discord Server: https://discord.gg/FNNNgqb')
	print('Github Link: https://github.com/Habchy/BasicBot')
	print('--------')
	print('Created by Habchy#1665')

def checkArgs(message, nbArgs, help):
    arrayArgs = message.split(" ")
    if(len(arrayArgs) < nbArgs):
        embed = discord.Embed(color=0xff0000)
        embed.add_field(
            name="Erreur",
            value=help,
            inline=True)
        return embed

def getUser(args, message, indexUser):
    userId = None
    if len(args) >= (indexUser+1):
        userId = extractId(args[indexUser])
    if userId is None:
        userId = message.author.id
    return userId


def extractId(args):
    userId = None
    if args.startswith("<@!"):
        userId = args[3:-1]
    elif args.startswith("<@"):
        userId = args[2:-1]
    print("Debug userid")
    print(args)
    print(userId)
    return userId

def getUserValue(message):
    arrayArgs = message.split(" ")
    return extractId(arrayArgs[2]), int(arrayArgs[3])

def getValue(message):
    arrayArgs = message.split(" ")
    return int(arrayArgs[2])

def getUserValueStr(message):
    arrayArgs = message.split(" ")
    return extractId(arrayArgs[2]), arrayArgs[3]

def getValueStr(message):
    arrayArgs = message.split(" ")
    return arrayArgs[2]

def makeTimeOperation(deltaMinutes, message, theSettings, embed):
    result = False
    if (message.author.id == MJ_ID):
        delta = 0
        try:
            delta = int(deltaMinutes)
        except ValueError:
            print("Not an integer")
            return
        if delta > 0:
            currentTime = theSettings.addTime(delta)
            result = True
            embed.add_field(
                name=("Temps ajouté"),
                value="<@" + message.author.id + "> a demandé l'ajout de " + deltaMinutes + " minutes.\nNous sommes donc maintenant le " + currentTime.strftime("%d/%m/%Y") + " à " + currentTime.strftime("%H:%M") + ".",
                inline=False)
    return result

def applyHeal(embed, user, value):
    testDb = CharacterDBHandler()
    remainingLife = testDb.increaseEv(user,value)
    embed.add_field(
        name=("Soin enregistrée"),
        value="Le joueur <@" + user + "> a soigné " + str(
            value) + " points de vie.\nIl reste " + remainingLife + " points de vie.",
        inline=False)


def applyInjury(embed, user, value):
    testDb = CharacterDBHandler()
    remainingLife = testDb.decreaseEv(user,value)
    embed.add_field(
        name=("Blessure enregistrée"),
        value="Le joueur <@" + user + "> a recu " + str(
            value) + " points de dégats.\nIl reste " + remainingLife + " points de vie.",
        inline=False)

def roll(diceCommand):
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

def handleInsults(message):
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

@client.event
async def on_message(message):
    resultInsult, gif = handleInsults(message)
    if resultInsult:
        await client.send_message(message.channel, content=gif[random.randint(0, len(gif)-1)])
        return
    if message.content.startswith('!pereBlaise') or message.content.startswith('!PereBlaise') or message.content.startswith('!PèreBlaise') or message.content.startswith('!pèreBlaise'):
        await client.send_message(message.channel, content="Hello jeune aventurier!\nJe ne te comprends pas. Va donc voir le channel <#"+HELP_CHANNEL+">")
    elif message.content.startswith('pereBlaise') or message.content.startswith('PereBlaise') or message.content.startswith('PèreBlaise') or message.content.startswith('pèreBlaise') or message.content.startswith('pB') or message.content.startswith('PB') or message.content.startswith('pb') or message.content.startswith('Pb'):
        args = message.content.split(" ")
        strContent = None
        embed = None
        if args[1] == 'test':
            userId = getUser(args, message, 2)
            testDb = CharacterDBHandler()
            if userId is not None:
                aChar = testDb.importCharacter(userId)
                embeds = testDb.displayInfoCharacter(aChar)
                embed = embeds[-1]
                for anEmbed in embeds[:-1]:
                    await client.send_message(message.channel, embed=anEmbed)
                testDb.decreaseEv(userId,70)

        elif args[1] == 'hi':
            embed = discord.Embed(description="I am pleased to welcome in this area !", color=0x00ff00)
            print(message.channel.id)

        elif args[1] == 'MJblessure':
            EmbedResult = checkArgs(message.content, 4, "Syntaxe: '!pereBlaise MJblessure <pseudo> <valeur>'")
            if EmbedResult is None and message.author.id==MJ_ID:
                user, value = getUserValue(message.content)
                embed = discord.Embed(color=0x00ff00)
                applyInjury(embed, user, value)
            else:
                embed=EmbedResult

        elif args[1] == 'MJsoin':
            EmbedResult = checkArgs(message.content, 4, "Syntaxe: '!pereBlaise MJsoin <pseudo> <valeur>'")
            if EmbedResult is None and message.author.name=="nogebour":
                user, value = getUserValue(message.content)
                embed = discord.Embed(color=0x00ff00)
                applyHeal(embed, user, value)
            else:
                embed=EmbedResult

        elif args[1] ==  'blessure':
            EmbedResult = checkArgs(message.content, 3, "Syntaxe: '!pereBlaise blessure <valeur>'")
            if EmbedResult is None:
                value = getValue(message.content)
                embed = discord.Embed(color=0x00ff00)
                applyInjury(embed, message.author.id, value)
            else:
                embed=EmbedResult

        elif args[1] == 'soin' or args[1] == 'soins':
            EmbedResult = checkArgs(message.content, 3, "Syntaxe: '!pereBlaise soin <valeur>'")
            if EmbedResult is None:
                value = getValue(message.content)
                embed = discord.Embed(color=0x00ff00)
                applyHeal(embed, message.author.id, value)
            else:
                embed=EmbedResult

        elif args[1] == 'liste' and (args[2] == "armes" or args[2] == "arme"):
            testDb = CharacterDBHandler()
            aChar = testDb.importCharacter(message.author.id)
            embeds = testDb.displayWeaponsCharacter(aChar)
            embed = embeds[-1]
            for anEmbed in embeds[:-1]:
                await client.send_message(message.channel, embed=anEmbed)

        elif args[1] == 'liste' and args[2] == "stuff":
            testDb = CharacterDBHandler()
            aChar = testDb.importCharacter(message.author.id)
            embeds = testDb.displayStuffCharacter(aChar)
            embed = embeds[-1]
            for anEmbed in embeds[:-1]:
                await client.send_message(message.channel, embed=anEmbed)

        elif args[1] == 'liste' and (args[2] == "skill" or args[2] == "skills"):
            testDb = CharacterDBHandler()
            aChar = testDb.importCharacter(message.author.id)
            embeds = testDb.displaySkillsCharacter(aChar)
            embed = embeds[-1]
            for anEmbed in embeds[:-1]:
                await client.send_message(message.channel, embed=anEmbed)

        elif args[1] == 'info':
            userId = message.author.id
            if len(args) > 2:
                tmpUserId = extractId(args[2])
                if tmpUserId is not None:
                    userId = tmpUserId
            testDb = CharacterDBHandler()
            aChar = testDb.importCharacter(userId)
            embeds = testDb.displayMinimumInfoCharacter(aChar)
            embed = embeds[-1]
            for anEmbed in embeds[:-1]:
                await client.send_message(message.channel, embed=anEmbed)

        elif args[1] == 'full' and (args[2] == 'info' or args[2] == 'infos'):
            testDb = CharacterDBHandler()
            aChar = testDb.importCharacter(message.author.id)
            embeds = testDb.displayInfoCharacter(aChar)
            embed = embeds[-1]
            for anEmbed in embeds[:-1]:
                await client.send_message(message.channel, embed=anEmbed)

        elif args[1] == 'bourse' and len(args) == 2:
            testDb = CharacterDBHandler()
            aChar = testDb.importCharacter(message.author.id)
            embed = testDb.displayMoneyInfos(aChar)

        elif args[1] == 'bourse':
            EmbedResult = checkArgs(message.content, 3, "Syntaxe: '!pereBlaise bourse <or>/<argent>/<bronze>'")
            if EmbedResult is None:
                value = getValueStr(message.content)
                testDb = CharacterDBHandler()
                gold, silver, bronze = testDb.moneyOperation(message.author.id, value)
                embed = discord.Embed(color=0x00ff00)
                embed.add_field(
                    name=("Operations comptables enregistrés"),
                    value="Le joueur "+message.author.name+" a "+str(gold)+" PO, "+str(silver)+" PA et "+str(bronze)+" PB.",
                    inline=False)
                await client.send_message(client.get_channel(MJ_CHANNEL), embed=embed, content="<@"+MJ_ID+">")
            else:
                embed=EmbedResult
        elif args[1] == 'MJbourse':
            EmbedResult = checkArgs(message.content, 4, "Syntaxe: '!pereBlaise MJbourse <user> <or>/<argent>/<bronze>'")
            if EmbedResult is None:
                user, value = getUserValueStr(message.content)
                testDb = CharacterDBHandler()
                gold, silver, bronze = testDb.moneyOperation(user, value)
                embed = discord.Embed(color=0x00ff00)
                embed.add_field(
                    name=("Operations comptables enregistrés"),
                    value="Le joueur <@"+user+"> a "+str(gold)+" PO, "+str(silver)+" PA et "+str(bronze)+" PB.",
                    inline=False)
                await client.send_message(client.get_channel(MJ_CHANNEL), embed=embed, content="<@"+MJ_ID+">")
            else:
                embed=EmbedResult
        elif args[1] == "temps" and len(args) == 2:
            theSettings = SettingsHandler()
            embed = discord.Embed(color=0x00ff00)
            embed.add_field(
                name=("Heure du jeu"),
                value="<@"+message.author.id+"> a demandé la date et on est le "+theSettings.current_time.strftime("%d/%m/%Y")+" à "+theSettings.current_time.strftime("%H:%M")+".",
                inline=False)

        elif args[1] == "temps" and args[2] == "passe" and len(args) == 3:
            theSettings = SettingsHandler()
            aDelta = theSettings.getElapsedTime()
            embed = discord.Embed(color=0x00ff00)
            embed.add_field(
                name=("Durée de l'aventure"),
                value=("Pour information l'aventure à commencé depuis "+str(aDelta)).replace("day", "jour"),
                inline=False)

        elif args[1] == "temps" and len(args) == 3:
            theSettings = SettingsHandler()
            embed = discord.Embed(color=0x00ff00)
            if(makeTimeOperation(args[2], message, theSettings, embed)):
                theSettings.saveSettings()

        elif args[1] == "temps" and len(args) == 5:
            if(args[2] == "repos" or args[2] == "marche"):
                theSettings = SettingsHandler()
                embed = discord.Embed(color=0x00ff00)
                if makeTimeOperation(args[4], message, theSettings, embed):
                    if args[2] == 'repos':
                        print("repos")
                        theSettings.handleRest(args[3], args[4], embed)
                    elif args[2] == 'marche':
                        print("Marche")
                        theSettings.handleWalk(args[3], args[4], embed)
        elif args[1] == "save":
            if message.author.id == MJ_ID:
                aDbHandler = DbHandler()
                aDbHandler.saveSnapshotGame()
        elif args[1] == "roll" and len(args) > 2:
            strContent = "<@"+message.author.id+">\n"+roll(args[2])
        else:
            strContent = "Hello jeune aventurier!\nJe ne te comprends pas. Va donc voir le channel <#"+HELP_CHANNEL+">"
        if not(strContent is None and embed is None):
            await client.send_message(message.channel, content=strContent, embed=embed)

client.run('MzgyNDY3Njc5ODc0NzExNTUz.DQNYmQ.0QJ6-j-wbo64BWYbri1vaT7Ndtw')

# Basic Bot was created by Habchy#1665
# Please join this Discord server if you need help: https://discord.gg/FNNNgqb
# Please modify the parts of the code where it asks you to. Example: The Prefix or The Bot Token
# This is by no means a full bot, it's more of a starter to show you what the python language can do in Discord.
# Thank you for using this and don't forget to star my repo on GitHub! [Repo Link: https://github.com/Habchy/BasicBot]

# The help command is currently set to be Direct Messaged.
# If you would like to change that, change "pm_help = True" to "pm_help = False" on line 9.