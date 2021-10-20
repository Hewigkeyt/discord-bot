import os
import re

#load modules and env
import discord
from discord import Status
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#setup discord client settings
intents = discord.Intents.default()
intents.members = True
intents.presences = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')
@client.event
async def on_message(msg):
    #test check members online
    if msg.content == '/online':
        total = 0
        online = 0
        for member in msg.guild.members:
            if not member.bot:
              total+=1
              if member.status != Status.offline:
                  online+=1
        await msg.reply("Total Members: "+ str(total) +" Online Members: " + str(online))
    #setup the categories and channels
    if msg.content == '/setup':
        guild = msg.guild
        categories = guild.categories
        channels = guild.channels

        #setup the category
        categoryExists = False
        for category in categories:
            if category.name == '\U0001F4C8 stats nulles \U0001F4C9':
                categoryExists = True
                statsCategory = category
                break
        if not categoryExists:
            statsCategory = await guild.create_category('\U0001F4C8 stats nulles \U0001F4C9')
        await statsCategory.move(beginning=True)

        #setup the channels
        channelTotalExists = False
        channelOnlineExists = False
        totalRe = re.compile('Nombre d\'ahuris: .+ \U0001F92A')
        onlineRe = re.compile('Ahuris online: .+ \U0001F92A\U0001F7E2')
        for channel in channels:
            if not channelTotalExists and totalRe.match(channel.name):
                channelTotalExists = True
                totalChannel = channel
            if not channelOnlineExists and onlineRe.match(channel.name):
                channelOnlineExists = True
                onlineChannel = channel

        total = 0
        online = 0
        for member in msg.guild.members:
            if not member.bot:
              total+=1
              if member.status != Status.offline:
                  online+=1

        if not channelTotalExists:
            totalChannel = await guild.create_voice_channel('Nombre d\'ahuris: '+str(total)+' \U0001F92A')
        if not channelOnlineExists:
            onlineChannel = await guild.create_voice_channel('Ahuris online: '+str(online)+' \U0001F92A\U0001F7E2')
        await totalChannel.edit(category=statsCategory,position=0)
        await onlineChannel.edit(category=statsCategory,position=1)
        await totalChannel.set_permissions(guild.default_role,connect=False)
        await totalChannel.set_permissions(guild.default_role,connect=False)

async def update_values(member):
    guild = member.guild
    channels = guild.channels
    total = 0
    online = 0
    for member in guild.members:
        if not member.bot:
            total+=1
            if member.status != Status.offline:
                online+=1
    channelTotalExists = False
    channelOnlineExists = False
    totalRe = re.compile('Nombre d\'ahuris: .+ \U0001F92A')
    onlineRe = re.compile('Ahuris online: .+ \U0001F92A\U0001F7E2')
    for channel in channels:
        if not channelTotalExists and totalRe.match(channel.name):
            channelTotalExists = True
            totalChannel = channel
        if not channelOnlineExists and onlineRe.match(channel.name):
            channelOnlineExists = True
            onlineChannel = channel
    if channelTotalExists:
        await totalChannel.edit(name='Nombre d\'ahuris: '+str(total)+' \U0001F92A')
    if channelOnlineExists:
        await onlineChannel.edit(name='Ahuris online: '+str(online)+' \U0001F92A\U0001F7E2')


@client.event
async def on_member_join(member):
    await update_values(member)

@client.event
async def on_member_remove(member):
    await update_values(member)

@client.event
async def on_member_update(before, after):
    guild = after.guild
    channels = guild.channels
    online = 0
    for member in guild.members:
        if not member.bot:
          if member.status != Status.offline:
              online+=1

    channelOnlineExists = False
    onlineRe = re.compile('Ahuris online: .+ \U0001F92A\U0001F7E2')
    for channel in channels:
        if onlineRe.match(channel.name):
            channelOnlineExists = True
            onlineChannel = channel
            break
    if channelOnlineExists:
        await onlineChannel.edit(name='Ahuris online: '+str(online)+' \U0001F92A\U0001F7E2')


client.run(TOKEN)

