import inspect
import discord
import asyncio
import urllib
from datetime import datetime
from discord.ext import commands
from discord.ext.commands import bot
from helper_functions import db_access as db
from helper_functions import reddit_helpers as rh


bot = commands.AutoShardedBot(command_prefix='/r/')


def discord_auth():
    # get discord credentials
    d_token_file = open("dToken.txt", "r")
    d_token = d_token_file.readline()
    d_token_file.close()
    return d_token


async def post_links(ctx, posts):
    for post in posts:

        # embed gif and text reminding users that nsfw is not allowed in a non-nsfw channel
        # embed = discord.Embed(title=post.title,
                              color = discord.Colour.magenta())
        # embed.set_image(url=post.url)
        # embed.set_image(url=post.url)
        # await ctx.send(embed=embed)

        # don't use embed for now
        await ctx.send(post.title + "\n" + post.url)

        await asyncio.sleep(1)


async def print_reddit_results(ctx, subreddit_name, reddit, num):

    if not db.verify_record(ctx.guild.id):
        await settings_default_notification(ctx)

    settings=db.get_settings(ctx.guild.id)

    if not rh.check_exists(subreddit_name):
        await ctx.send(f"Subreddit [/r/{subreddit_name}] doesn't exist.")
        return

    subreddit=reddit.subreddit(subreddit_name)

    # check that we have access to posts on the subreddit
    accessible, accessibility_message=rh.subreddit_accessible(subreddit)
    if not accessible:
        await ctx.send(accessibility_message)
        return

        # stop executing if nsfw is not allowed to be posted here
    if subreddit.over18:
        if (await check_nsfw_allowed(ctx, settings)) == False:
            return

    # if no results length given use server default
    if (num == ""):
        num=int(settings[0][0])

    num=int(num)

    if num <= settings[0][1]:

        # sort type is the name of the calling fucntion as a string
        sort_type=inspect.stack()[1][3]
        # get get [num] posts from [sort_type] on [subreddit]
        result_list=rh.get_nonsticky_submissions(
            subreddit, f"{sort_type}", num)
        await post_links(ctx, result_list)
    else:
        await ctx.send(f"This server caps the number of results requested at {settings[0][1]}")


async def check_nsfw_allowed(ctx, settings):
    # start with allowed being true and set false if any disqualifying criteria are met, prints all relevant warnings
    allowed = True

    # if channel is not tagged nsfw set alllowed to false
    if not ctx.channel.is_nsfw():
        await nsfw_warning(ctx)
        allowed = False

    # if the setting nsfw_restricted is set to true set allowed to false
    if settings[0][2]:
        await ctx.send(f"NSFW subreddits are restricted in this server. Admins may adjust this with /r/toggle_nsfw.")
        allowed = False

    return allowed


async def nsfw_warning(ctx):
    # embed gif and text reminding users that nsfw is not allowed in a non-nsfw channel
    embed = discord.Embed(title="NSFW subreddits",
                          color=discord.Colour.magenta())
    embed.description = "NSFW content is not allowed outside of channels tagged NSFW. Servers staff can change this in channel settings."
    embed.set_image(url="https://i.imgur.com/oe4iK5i.gif")
    await ctx.send(embed=embed)


async def output_db(ctx):
    # output tabulated results of SELECT * FROM servers, should only ever be referenced from DEBUG cog and if user using it is the developer (me)
    output_string = "```server_id\t\t\t default_results\tmax_results\tnsfw_restricted"
    all_rows = db.get_all()
    for row in all_rows:
        output_string += f"\n{row[0]}\t{row[1]}\t\t\t\t  {row[3]}\t\t\t {row[2]}"
    output_string += "```"
    await ctx.send(output_string)


async def access_warning(ctx):
    # warn users who have discovered the database_dump command on github that they are not permitted to access that information and that the attemp has been logged
    guild_id,  guild_name = {ctx.guild.id, ctx.guild.name}
    user_id, user_name = {ctx.message.author.id, ctx.message.author.name}
    timestamp = datetime.now().strftime("%Y/%m/%d, %H:%M")
    log_item = f"Attempted unauthorised database access by USER=[{user_id} - {user_name}] in SERVER=[{guild_id} - {guild_name}] at TIME=[{timestamp}]\n"

    # write to a log file
    with open("incident_log.txt", "a") as log:
        log.write(log_item)
        log.close()

    # send a log to me
    dev = bot.get_user(230723477630353408)
    await dev.send(log_item)

    await ctx.send(log_item)
    await ctx.send("This is a secure command for debug and development purposes only. You are not permitted to access the database. This action has been logged.")


async def settings_default_notification(ctx):

    log_item = f"DB Error: missing row for {ctx.guild.id}"
    print(log_item)
    with open("db_log.txt", "a") as log:
        log.write(log_item)
        log.close()
    await ctx.send("Your settings record could not be verified in the database and has been reset to the default (default number of posts = 5, max posts = 20, nsfw_restricted = true). Use the / r / help command to see how to set your settings back to how you want them.Sorry for the inconvenience. ")
