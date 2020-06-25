import discord
from discord.ext import commands
import praw
from helper_functions import reddit_helpers as rh
from helper_functions import discord_helpers as dh


class Standard(commands.Cog):
    reddit = rh.reddit_auth()

    def __intit__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, hidden=True)
    async def ping(self, ctx):
        await ctx.send("pong!")

    @commands.command(pass_context=True)
    async def hot(self, ctx, subreddit_name, num=5):
        subreddit = self.reddit.subreddit(subreddit_name)
        # get get [num] posts from [hot] on [subreddit]
        hot_list = rh.get_nonsticky_submissions(subreddit, "hot", num)
        await dh.post_links(ctx, hot_list)

    @commands.command(pass_context=True)
    async def new(self, ctx, subreddit_name, num=5):
        subreddit = self.reddit.subreddit(subreddit_name)
        # get get [num] posts from [new] on [subreddit]
        new_list = rh.get_nonsticky_submissions(subreddit, "new", num)
        await dh.post_links(ctx, new_list)

    @commands.command(pass_context=True)
    async def top(self, ctx, subreddit_name, num=5):
        subreddit = self.reddit.subreddit(subreddit_name)
        # get get [num] posts from [top] on [subreddit]
        top_list = rh.get_nonsticky_submissions(subreddit, "top", num)
        await dh.post_links(ctx, top_list)

    @commands.command(pass_context=True)
    async def controversial(self, ctx, subreddit_name, num=5):
        subreddit = self.reddit.subreddit(subreddit_name)
        # get get [num] posts from [top] on [subreddit]
        cont_list = rh.get_nonsticky_submissions(
            subreddit, "controversial", num)
        await dh.post_links(ctx, cont_list)

    @commands.command(pass_context=True)
    async def random(self, ctx, subreddit_name):
        subreddit = self.reddit.subreddit(subreddit_name)
        rand_post = subreddit.random()
        await ctx.send(rand_post.title + "\n" + rand_post.url)


def setup(bot):

    bot.add_cog(Standard(bot))
