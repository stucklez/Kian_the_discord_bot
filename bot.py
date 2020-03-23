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
GUILD_ID = os.getenv('DISCORD_GUILD')

kian_quotes = []
quotesfile = open("quotes.txt","r")
kian_quotes = quotesfile.readlines()
quotesfile.close()

play_queue = []
print(f'{kian_quotes}\n')

#Emojis for reactions
like = '\U0001F44D'
letter = '\U0001F48C'
horn_emote = '\U0001F4EF'
comet = '\U00002604'
cry = '\U0001F622'

bot = commands.Bot(command_prefix = '<3')

@bot.command()
async def stop(ctx):
    await ctx.voice_client.stop()

@bot.command()
async def pause(ctx):
    if ctx.voice_client is None or ctx.voice_client.is_playing() is False:
        await ctx.channel.send('Not playing anything')
    else:
        await ctx.voice_client.pause()

@bot.command()
async def resume(ctx):
    if ctx.voice_client is not None or ctx.voice_client.is_playing() is True:
        await ctx.channel.send('Already playing')
    else:
        await ctx.voice_client.resume()

@bot.command()
async def oof(ctx):
    print(f'joining')
    oof = FFmpegPCMAudio('Roblox Death Sound (Oof).mp3')
    if ctx.voice_client is not None:
        ctx.voice_client.play(oof)
    else:
        channel = ctx.message.author.voice.channel
        vc = await channel.connect()
        vc.play(oof)
    while vc.is_playing():
        True
    await ctx.message.add_reaction(comet)
    await vc.disconnect()

@bot.command()
async def horn(ctx):
    print(f'joining')
    horn = FFmpegPCMAudio('mlg-airhorn.mp3')
    if ctx.voice_client is not None:
        ctx.voice_client.play(horn)
    else:
        channel = ctx.message.author.voice.channel
        vc = await channel.connect()
        vc.play(horn)
    while vc.is_playing():
        True
    await ctx.message.add_reaction(horn_emote)
    await vc.disconnect()


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
    while vc.is_playing():
        True
    await ctx.message.add_reaction(letter)
    await vc.disconnect()

@bot.command()
async def leave(ctx):
    vc = bot.voice_clients
    for i in vc:
        if i.guild == ctx.message.channel.guild:
            await i.disconnect()
        else:
            await ctx.channel.send('Not connected to voice channel')

@bot.command()
async def ping(ctx):
    print(f'Ping')
    await ctx.channel.send(f'Ping {round(bot.latency * 1000)}')

@bot.command()
async def quote_add(ctx):
    server_id = ctx.message.guild.id
    if str(server_id) == GUILD_ID:
        quote = ctx.message.content
        string_split = quote.split(" ")
        string_split.remove('<3quote_add')
        new_quote = ""
        for string in string_split:
            new_quote += string + " "
        kian_quotes.append(new_quote)
        quotesfile = open("quotes.txt", "a")
        quotesfile.write(f'\n{new_quote}')
        quotesfile.close()
        await ctx.message.add_reaction(like)
    else:
        await ctx.channel.send('Not connected to the right server')

@bot.command()
async def quote(ctx):
    server_id = ctx.message.guild.id
    if str(server_id) == GUILD_ID:
        response = random.choice(kian_quotes)
        await ctx.channel.send(response)
    else:
        await ctx.channel.send('Not connected to the right server')

@bot.event
async def on_ready():
    print('Ready')

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'HELLO {member.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    f_in_chat = message.content.split(" ")
    for i in f_in_chat:
        if i.lower() == 'f':
            await message.channel.send('F') 

    if 'kian kan' in message.content.lower() or 'kian må' in message.content.lower() or 'kian skal' in message.content.lower():
        choice = random.randint(1, 2)
        if choice is 1:
            await message.channel.send('Ja')
        elif choice is 2:
            await message.channel.send('Nej')
    
    if 'nemt kian' in message.content.lower():
        await message.channel.send('ALTID')

    
    await bot.process_commands(message)

bot.run(TOKEN)
