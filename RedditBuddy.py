import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import bot
import praw
import reddit_helpers as rh

# get reddit credentials
reddit_token_file = open("redditSecrets.txt", "r")
r_id = reddit_token_file.readline().rstrip()
r_secret = reddit_token_file.readline().rstrip()
r_usersubreddit_name = reddit_token_file.readline().rstrip()
r_password = reddit_token_file.readline().rstrip()
reddit_token_file.close()

# reddit authentication
reddit = praw.Reddit(client_id=r_id, client_secret=r_secret,
                     password=r_password, user_agent='USERAGENT',
                     usersubreddit_name=r_usersubreddit_name)

# get discord credentials
d_token_file = open("dToken.txt", "r")
d_token = d_token_file.readline()
d_token_file.close()

client = discord.Client()
bot = commands.Bot(command_prefix='/r/')


@bot.event
async def on_ready():
    print("Reddit Buddy online!")


@bot.command(pass_context=True, hidden=True)
async def ping(ctx):
    await ctx.send("pong!")


@bot.command(pass_context=True)
async def hot(ctx, subreddit_name, num=5):
    subreddit = reddit.subreddit(subreddit_name)
    # get get [num] posts from [hot] on [subreddit]
    hot_list = rh.get_nonsticky_submissions(subreddit, "hot", num)
    await post_links(ctx, hot_list)


@bot.command(pass_context=True)
async def new(ctx, subreddit_name, num=5):
    subreddit = reddit.subreddit(subreddit_name)
    # get get [num] posts from [new] on [subreddit]
    new_list = rh.get_nonsticky_submissions(subreddit, "new", num)
    await post_links(ctx, new_list)


@bot.command(pass_context=True)
async def top(ctx, subreddit_name, num=5):
    subreddit = reddit.subreddit(subreddit_name)
    # get get [num] posts from [top] on [subreddit]
    top_list = rh.get_nonsticky_submissions(subreddit, "top", num)
    await post_links(ctx, top_list)


@bot.command(pass_context=True)
async def controversial(ctx, subreddit_name, num=5):
    subreddit = reddit.subreddit(subreddit_name)
    # get get [num] posts from [top] on [subreddit]
    cont_list = rh.get_nonsticky_submissions(subreddit, "controversial", num)
    await post_links(ctx, cont_list)


@bot.command(pass_context=True)
async def random(ctx, subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)
    rand_post = subreddit.random()
    await ctx.send(rand_post.title + "\n" + rand_post.url)


async def post_links(ctx, posts):
    for post in posts:
        await ctx.send(post.title + "\n" + post.url)


# authenticate and run discord bot
bot.run(d_token)
