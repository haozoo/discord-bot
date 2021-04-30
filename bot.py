import discord
import os
from utils import fun
from utils import riot
from dotenv import load_dotenv
from discord.ext import commands


# Load environment variables
load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')


@bot.command()
async def checklevel(ctx, ign):
    await ctx.send(riot.printplayer(ign))


@bot.command()
async def checkrank(ctx, ign, queuetype):
    await ctx.send(riot.printrank(ign, queuetype))


@bot.command()
async def lastmatch(ctx, ign):
    await ctx.send(riot.printlastmatch(ign))


@bot.command()
async def encode(ctx, text):
    await ctx.message.channel.send(ctx.message.author.name + ' has encoded the following message:\n' + fun.coder(text))
    await ctx.message.delete()


@bot.command()
async def decode(ctx, text):
    await ctx.message.channel.send('Your decoded message is:\n' + fun.coder(text))


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

bot.run(DISCORD_TOKEN)
