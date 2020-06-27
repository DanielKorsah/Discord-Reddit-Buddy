from helper_functions import reddit_helpers as rh
from helper_functions import discord_helpers as dh
from helper_functions import db_access as db


class Standard(dh.commands.Cog):
    reddit = rh.reddit_auth()

    def __intit__(self, bot):
        self.bot = bot

    @dh.commands.command(pass_context=True)
    async def hot(self, ctx, subreddit_name, number_of_results=""):
        await dh.print_reddit_results(ctx, subreddit_name,
                                      self.reddit, number_of_results)

    @dh.commands.command(pass_context=True)
    async def new(self, ctx, subreddit_name, number_of_results=""):
        await dh.print_reddit_results(ctx, subreddit_name,
                                      self.reddit, number_of_results)

    @dh.commands.command(pass_context=True)
    async def top(self, ctx, subreddit_name, number_of_results=""):
        await dh.print_reddit_results(ctx, subreddit_name,
                                      self.reddit, number_of_results)

    @dh.commands.command(pass_context=True)
    async def controversial(self, ctx, subreddit_name, number_of_results=""):
        await dh.print_reddit_results(ctx, subreddit_name,
                                      self.reddit, number_of_results)

    @dh.commands.command(pass_context=True)
    async def random(self, ctx, subreddit_name):

        subreddit = self.reddit.subreddit(subreddit_name)

        # stop executing if nsfw is not allowed to be posted here
        if subreddit.over18:
            if (await dh.check_nsfw_allowed(ctx, db.get_settings(ctx.guild.id)[0][2])) == False:
                return

        rand_post = subreddit.random()
        await ctx.send(rand_post.title + "\n" + rand_post.url)


def setup(bot):
    bot.add_cog(Standard(bot))
    print("Cog Loaded: Standard")
