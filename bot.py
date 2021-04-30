import discord
import os
import riots
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()


def coder(string):
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
        if letter in dict:
            message = message + dict[letter]
        else:
            message = message + 'x'

    return message


@ client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@ client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!encode'):
        await message.channel.send(message.author.name + ' has encoded the following message:\n' + coder(message.content))
        await message.delete()

    if message.content.startswith('!decode'):
        await message.channel.send('Your decoded message is:\n' + coder(message.content))

    if message.content.startswith('!checklevel'):
        ign = message.content.split(' ', 1)[1]
        await message.channel.send(riots.printplayer(ign))

    if message.content.startswith('!checkrank'):
        ign = message.content.split(' ', 1)[1]
        await message.channel.send(riots.printrank(ign))

    if message.content.startswith('!lastmatch'):
        ign = message.content.split(' ', 1)[1]
        await message.channel.send(f"Here are the details of {ign}\'s last match:\n" + riots.printlastmatch(ign))

client.run(DISCORD_TOKEN)
