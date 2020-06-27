import inspect
import discord
from discord.ext import commands
from discord.ext.commands import bot
from helper_functions import db_access as db
from helper_functions import reddit_helpers as rh


def discord_auth():
    # get discord credentials
    d_token_file = open("dToken.txt", "r")
    d_token = d_token_file.readline()
    d_token_file.close()
    return d_token


async def post_links(ctx, posts):
    for post in posts:
        await ctx.send(post.title + "\n" + post.url)


async def print_reddit_results(ctx, subreddit_name, reddit, num):

    # explicity cast to int

    settings = db.get_settings(ctx.guild.id)
    subreddit = reddit.subreddit(subreddit_name)

    # stop executing if nsfw is not allowed to be posted here
    if subreddit.over18:
        if (await check_nsfw_allowed(ctx, settings)) == False:
            return

    # if no results length given use server default
    if (num == ""):
        num = int(settings[0][0])

    num = int(num)

    if num < settings[0][1]:

        # sort type is the name of the calling fucntion as a string
        sort_type = inspect.stack()[1][3]
        # get get [num] posts from [sort_type] on [subreddit]
        result_list = rh.get_nonsticky_submissions(
            subreddit, f"{sort_type}", num)
        await post_links(ctx, result_list)
    else:
        await ctx.send(f"This server caps the number of results requested at {settings[0][1]}")


async def check_nsfw_allowed(ctx, settings):
    # start with allowed being true and set false if any disqualifying criteria are met
    # prints all relevant warnings
    allowed = True

    if not ctx.channel.is_nsfw():
        await nsfw_warning(ctx)
        allowed = False

    if not settings[0][2]:
        await ctx.send(f"NSFW subreddits are restricted in this server. Admins may adjust this with /r/toggle_nsfw.")
        allowed = False

    return allowed


async def nsfw_warning(ctx):
    embed = discord.Embed(title="NSFW subreddits",
                          color=discord.Colour.magenta())
    embed.description = "NSFW content is not allowed outside of channels tagged NSFW. Servers staff can change this in channel settings."
    embed.set_image(url="https://i.imgur.com/oe4iK5i.gif")
    await ctx.send(embed=embed)
