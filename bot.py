import urllib.request
import json
from urllib.parse import unquote
import os
import random
import datetime

# discord library
import discord
from discord.ext import commands

# local Running Library
from dotenv import load_dotenv
load_dotenv()

# get token
try:
    token = os.environ.get('DISCORD_TOKEN')
    print("success get token")
except:
    token = os.getenv('DISCORD_TOKEN')
    print("This bot running from localhost")


# instance object called 'bot'
bot_prefix = '!'
bot = commands.Bot(command_prefix=bot_prefix)
bot.description = "Bot for find price on http://www.romexchange.com"
bot.activity = discord.Activity(name="!cek", detail="!cek", type=discord.ActivityType.listening, start=datetime.datetime.now())

# pesan = commands.DefaultHelpCommand(dm_help=True)
# bot.help_command = pesan

# Fungsi untuk callback jika bot berhasil koneksi ke discord server
@bot.event
async def on_ready():
    print(f'{bot.user.name} is connected')
    # for guild in bot.guilds:
    #     print(guild, guild.member_count)
    
# Fungsi untuk mengirim pesan ketika member bergabung ke dalam server
@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

# Fungsi untuk mengambil harga barang dari website romexchange
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

# Fungsi untuk error reporting
@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

# Fungsi untuk error reporting
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

@bot.command()
async def info(ctx):
    embed = discord.Embed(title="SmokieBot", description=bot.description, color=0xeee657)

    # give info about you here
    embed.add_field(name="Author", value="Donat#4054")

    # Shows the number of servers the bot is member of.
    embed.add_field(name="Server count", value=f"{len(bot.guilds)}")

    # give users a link to invite thsi bot to their server
    embed.add_field(name="Invite", value="[Add SmokieBot](https://discordapp.com/api/oauth2/authorize?client_id=618658270323933199&permissions=251968&scope=bot)")

    await ctx.send(embed=embed)

bot.remove_command('help')
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="SmokieBot", description=bot.description+". List of commands are:", color=0xeee657)
    
    embed.add_field(name=bot_prefix+"cek [item-name]", value="Find price of items with given names (example: "+bot_prefix+"cek minorous card)", inline=False)
    embed.add_field(name=bot_prefix+"info", value="Gives a little info about the bot", inline=False)
    embed.add_field(name=bot_prefix+"help", value="Gives this message", inline=False)

    await ctx.author.send(embed=embed)
    await ctx.send(embed=embed)

# @bot.command()
# async def prefix(ctx, arg):
#     bot.command_prefix = arg

#     await ctx.send("bot prefix change to" + arg)

bot.run(token)
