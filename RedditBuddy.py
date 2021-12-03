#!/usr/local/bin/python3.6
import os
from helper_functions import discord_helpers as dh


discord = dh.discord

bot = dh.bot


@bot.event
async def on_ready():
    # for each file in cogs directory
    for filename in os.listdir("./cogs"):
        # if it's a python file, try to load it as a discord cog
        if filename.endswith(".py"):
            try:
                bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"Cog Loaded: {filename[:-3]}")
            except:
                print(f"Cog {filename[:-3]} already loaded or doesn't exist.")

    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Praise Geraldo"))
    print("Reddit Buddy online!")
    print(f"active in {len(bot.guilds)} servers")


if __name__ == "__main__":
    # authenticate and run discord bot
    bot.run(dh.discord_auth())
