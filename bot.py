import discord
import os
from dotenv import load_dotenv
import random
import cassiopeia as cass


# Load environment variables
load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
LOL_API_KEY = os.getenv('LEAGUE_API')
client = discord.Client()


def decoder(string):
    dict = {'Q': '%', 'W': '^', 'E': '~', 'R': '|', 'T': '[',
            'Y': ']', 'U': '<', 'I': '>', 'O': '{', 'P': '}',
            'A': '@', 'S': '#', 'D': '&', 'F': '*', 'G': '-',
            'H': '+', 'J': '=', 'K': '(', 'L': ')', 'Z': '_',
            'X': '$', 'C': '"', 'V': '\'', 'B': ':', 'N': ';',
            'M': '/',
            '1': ',', '2': '.', '3': '!', '4': '?',
            '%': 'Q', '^': 'W', '~': 'E', '|': 'R', '[': 'T',
            ']': 'Y', '<': 'U', '>': 'I', '{': 'O', '}': 'P',
            '@': 'A', '#': 'S', '&': 'D', '*': 'F', '-': 'G',
            '+': 'H', '=': 'J', '(': 'K', ')': 'L', '_': 'Z',
            '$': 'X', '"': 'C', '\'': 'V', ':': 'B', ';': 'N',
            '/': 'M',
            ',': '1', '.': '2', '!': '3', '?': '4',
            ' ': '  '}

    string = string[8:].upper()
    message = ''

    for letter in string:
        message = message + dict[letter]

    return message


# This overrides the value set in your configuration/settings.
def league(sumname):
    sumname = sumname[11:]
    cass.set_riot_api_key(LOL_API_KEY)
    cass.set_default_region("OCE")

    summoner = cass.get_summoner(name=sumname)
    message = ("This loser, {name} is a summoner on the {region} server.".format(name=summoner.name,
                                                                                 region=summoner.region))
    return message


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!encode'):
        await message.channel.send('Your encoded message is:\n' + decoder(message.content))

    if message.content.startswith('!decode'):
        await message.channel.send('Your decoded message is:\n' + decoder(message.content))

    if message.content.startswith('!lllsearch'):
        await message.channel.send(league(message.content))

client.run(DISCORD_TOKEN)
