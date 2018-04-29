# These are the dependecies. The bot depends on these to function, hence the name.
# Please do not change these unless your adding to them, because they can break the bot.
import os
import platform

import discord #noinspection
from discord.ext.commands import Bot #noinspection

from src.PereBlaiseBot import PereBlaiseBot

# Here you can modify the bot's prefix and description and wether it sends help in direct messages or not.
client = Bot(description="Basic Bot by Habchy#1665", command_prefix="/Blaise:", pm_help = True)

HELP_CHANNEL = '387149097037070346'
MJ_CHANNEL = '386082775066869760'
MJ_ID = '294164488427405312'

theBot = PereBlaiseBot()

# This is what happens everytime the bot launches.
# In this case, it prints information like :
#  * server count
#  * user count the bot is connected to
#  * the bot id in the console.
# Do not mess with it because the bot can break, if you wish to do so, please consult me or someone trusted.


@client.event
async def on_ready():
    print('Logged in as '+client.user.name+' (ID:'+client.user.id+') |'
          ' Connected to '+str(len(client.servers))+' servers |'
          ' Connected to '+str(len(set(client.get_all_members())))+' users')
    print('--------')
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__,
                                                                               platform.python_version()))
    print('--------')
    print('Use this link to invite {}:'.format(client.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
    print('--------')
    print('Support Discord Server: https://discord.gg/FNNNgqb')
    print('Github Link: https://github.com/Habchy/BasicBot')
    print('--------')
    print('Created by Habchy#1665')

@client.event
async def on_message(message):
    result_messages = theBot.on_message(message, client)
    for aMessage in result_messages:
        await client.send_message(aMessage.discordChannel, embed=aMessage.embedMessage, content=aMessage.strMessage)

client.run(os.environ['TOKEN'])
