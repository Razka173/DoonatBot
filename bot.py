import urllib.request, json
from urllib.parse import unquote
import os
import sys
import random

# Discord Library
import discord
from discord.ext import commands

# Discord Presence
from pypresence import Presence
import time

# For local running
# from dotenv import load_dotenv
# load_dotenv()
# token = os.getenv('DISCORD_TOKEN')
# GUILD = os.getenv('DISCORD_GUILD')

# For heroku running, put your token into environment variable
#token = sys.argv[1]
token = os.environ.get('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} is connected')

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@bot.command(name='cek')
async def cek_harga(ctx, *, keyword):
    var_item = urllib.parse.quote(keyword)
    var_slim = "&slim=true"
    var_exact = "&exact=false"
    link = "https://www.romexchange.com/api?item=" + var_item + var_slim + var_exact
    with urllib.request.urlopen(link) as url:
        data = json.loads(url.read().decode())
        arraydata = list()
        if len(data) == 0:
            response = "No Item Found"
        else:
            for i in range (len(data)):
                nama_barang = data[i].get("name")
                harga_sea = data[i].get("sea").get("latest") #int
                display_harga = "{:,}".format(harga_sea) + "_z_"
                price_change = data[i].get("sea").get("week")["change"] #float type
                if price_change > 0:
                    format_price_change = "+" + str(price_change) + "%"
                else:
                    format_price_change = str(price_change) + "%"
                temp_memory = dict(nama_barang=nama_barang, harga_sea=display_harga, week_change=format_price_change)
                arraydata.append(temp_memory)
            if arraydata == None:
                response = "No Item Found"
            else:
                response = ""
                for data in arraydata:
                    response += "**__" + data.get("nama_barang") + "__**" + "\n"
                    response += "SEA Price: " + data.get("harga_sea")
                    response += " (" + data.get("week_change") + " this week)" + "\n \n"
        print("operation success")
        await ctx.send(response)

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

bot.run(token)