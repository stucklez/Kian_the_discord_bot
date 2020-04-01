# bot.py
#import modules
import os
import pymongo
import random
import discord
import shlex
from discord.ext import commands
from discord import FFmpegPCMAudio
from dotenv import load_dotenv
import helperfunctions as hp
import classes as classes


#loading enviroment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILD_ID = os.getenv('DISCORD_GUILD')
MONGO_URI = os.getenv('MONGO_URI')

dbclient = pymongo.MongoClient(MONGO_URI)
db = dbclient.Kian
quotes_col = db.Quotes
movies_col = db.Movies

#reading elements from the database
kian_quotes = hp.initquotes(quotes_col)
kian_movies = hp.initmovies(movies_col)

for i in kian_quotes:
    print(f'{i.quote}')
for i in kian_movies:
    print(f'{i.title}')

#Emojis for reactions
like = '\U0001F44D'
letter = '\U0001F48C'
horn_emote = '\U0001F4EF'
comet = '\U00002604'
cry = '\U0001F622'
movie_emote = '\U0001F3A5'

bot = commands.Bot(command_prefix = '<3')


#commands which trigger when the prefix <3 is used

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
async def bonk(ctx):
    print(f'joining')
    bonk = FFmpegPCMAudio('Bonk Sound Effect #2.mp3')
    if ctx.voice_client is not None:
        ctx.voice_client.play(horn)
    else:
        channel = ctx.message.author.voice.channel
        vc = await channel.connect()
        vc.play(bonk)
    while vc.is_playing():
        True
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
        new_quote = hp.get_quote(ctx.message.content)
        document = {"Author": new_quote.author,
                    "Quote": new_quote.quote}
        _id = quotes_col.insert_one(document).inserted_id
        new_quote._id = _id
        kian_quotes.append(new_quote)
        await ctx.message.add_reaction(like)
    else:
        await ctx.channel.send('Not connected to the right server')

@bot.command()
async def quote(ctx):
    server_id = ctx.message.guild.id
    if str(server_id) == GUILD_ID:
        response = random.choice(kian_quotes)
        await ctx.channel.send(f'{response.author} - {response.quote}')
    else:
        await ctx.channel.send('Not connected to the right server')

@bot.command()
async def list_movies(ctx):
    send_string = ""
    for i in kian_movies:
        if i.server == ctx.message.guild.id:
            send_string += i.title + "\n"
    await ctx.channel.send(f'List of movies\n{send_string}')
@bot.command()
async def add_movie(ctx):
    movie = hp.get_movie(ctx.message.content)
    movie.server = ctx.message.guild.id
    document = {"Title": movie.title,
                "Genre": movie.genre, 
                "Year": movie.year, 
                "Server": movie.server}
    _id = movies_col.insert_one(document).inserted_id
    movie._id = _id
    kian_movies.append(movie)
    await ctx.message.add_reaction(movie_emote)

@bot.command()
async def movie(ctx):
    response = hp.choose_by_genre(kian_movies, ctx.message.guild.id)
    if response is not None:
        kian_movies.remove(response)
        delete_query = {"_id": response._id}
        movies_col.delete_one(delete_query)
        await ctx.channel.send(f'Tonights movie will be: {response.title}')
    else:
        await ctx.channel.send(f'There are no movies for this server')

@bot.command()
async def by_genre(ctx):
    string = ctx.message.content
    string_split = shlex.split(string)
    string_split.remove('<3by_genre')
    filtered_movies = []
    for i in kian_movies:
        if i.server == ctx.message.guild.id and i.genre == string_split[0].lower():
            filtered_movies.append(i)
    if len(filtered_movies) > 0:
        response = random.choice(filtered_movies)
        kian_movies.remove(response)
        delete_query = {"_id": response._id}
        movies_col.delete_one(delete_query)
        await ctx.channel.send(f'Tonights movie of genre {response.genre} will be: {response.title}')
    else:
        await ctx.channel.send(f'No movies of genre {string_split[0]}')


#event which triggers when the bot connects
@bot.event
async def on_ready():
    print('Ready')

#event which triggers and sends a message to a new user who joins the server
@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'HELLO {member.name}')

#events which trigger on specific messages written in text channels
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
        if choice == 1:
            await message.channel.send('Ja')
        elif choice == 2:
            await message.channel.send('Nej')
    
    if 'nemt kian' in message.content.lower():
        await message.channel.send('ALTID')

    #makes the bot listen for commands
    await bot.process_commands(message)

bot.run(TOKEN)
