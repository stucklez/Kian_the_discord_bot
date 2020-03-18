# bot.py
import os

import random
import discord
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

kian_quotes = []
quotesfile = open("quotes.txt","r")
kian_quotes = quotesfile.readlines()
quotesfile.close()

print(f'{kian_quotes}\n')

client = discord.Client()



@client.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'HELLO {member.name}, FUCK YOU')

@client.event
async def on_message(message):
    if message.author == client.user:
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

    if 'Kian kan man' in message.content.lower():
        choice = random.randrange(1, 2)
        if choice is 1:
            await message.channel.send('Ja')
        elif choice is 2:
            await message.channel.send('Nej')


client.run(TOKEN)