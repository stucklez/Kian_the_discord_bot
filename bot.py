# bot.py
import os

import random
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

kian_quotes = []
quotesfile = open("quotes.txt","r")
kian_quotes = quotesfile.readlines()
quotesfile.close()

print(f'{kian_quotes}\n')

bot = commands.Bot(command_prefix = '<3')

@bot.command()
async def brev(ctx):
    print(f'joining')
    brev = FFmpegPCMAudio('Der breeeeeev!.mp3')
    if ctx.voice_client is not None:
        ctx.voice_client.play(brev)
    else:
        channel = ctx.message.author.voice.channel
        vc = await channel.connect()
        vc.play(brev)

@bot.command()
async def leave(ctx):
    vc = bot.voice_clients
    for i in vc:
        if i.guild == ctx.message.channel.guild:
            await i.disconnect()
        else:
            ctx.channel.send('Not connected to voice channel')

@bot.command()
async def ping(ctx):
    print(f'Ping')
    await ctx.channel.send(f'Ping {round(bot.latency * 1000)}')

@bot.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD, bot.guilds)

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'HELLO {member.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == 'Kian! QUOTES!':
        response = random.choice(kian_quotes)
        await message.channel.send(response)

    if 'happy birthday' in message.content.lower():
        await message.channel.send('Happy Birthday! 🎈🎉')

    if '!quote' in message.content.lower():
        print(f'QUOTE')
        quote = message.content
        string_split = quote.split(" ")
        string_split.remove('!quote')
        new_quote = ""
        for string in string_split:
           new_quote += string + " "
        kian_quotes.append(new_quote)
        quotesfile = open("quotes.txt", "a")
        quotesfile.write(f'\n{new_quote}')
        quotesfile.close()
        print(f'{kian_quotes}\n')
    
    if message.author == 'GitHub':
        print('Github')
        await message.channel.send('!p https://www.youtube.com/watch?v=Vkvh2yd2cxY')

    if 'kian kan man' in message.content.lower():
        print(f'Kian kan man')
        choice = random.randint(1, 2)
        print(f'{choice}')
        if choice is 1:
            await message.channel.send('Ja')
        elif choice is 2:
            await message.channel.send('Nej')
    
    if 'nemt kian' in message.content.lower():
        await message.channel.send('ALTID')

    
    await bot.process_commands(message)

bot.run(TOKEN)
