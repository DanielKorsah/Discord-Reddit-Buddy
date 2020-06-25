import discord
from discord.ext import commands
from discord.ext.commands import bot


def discord_auth():
    # get discord credentials
    d_token_file = open("dToken.txt", "r")
    d_token = d_token_file.readline()
    d_token_file.close()
    return d_token


async def post_links(ctx, posts):
    for post in posts:
        await ctx.send(post.title + "\n" + post.url)
