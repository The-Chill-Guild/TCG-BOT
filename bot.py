import discord
from discord.ext import commands, tasks
from itertools import cycle
import asyncio
from dotenv import load_dotenv
import os

load_dotenv('.env')

bot = commands.Bot(command_prefix = '.', intents=discord.Intents.all())
bot_status = cycle(['DM ModMail', '.help'])

@tasks.loop(hours=1)
async def change_status():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="DM ModMail"))

@bot.event
async def on_ready():
    await bot.tree.sync()
    print('Bot is ready.')
    change_status.start()

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
           await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    async with bot:
        await bot.start(os.getenv('TOKEN')) 

asyncio.run(main())