import os
from helper_functions import discord_helpers as dh


discord = dh.discord
client = discord.Client()
bot = dh.commands.Bot(command_prefix='/r/')


@bot.event
async def on_ready():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")

    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Suppressing mutants"))
    print("Reddit Buddy online!")

# authenticate and run discord bot
bot.run(dh.discord_auth())
