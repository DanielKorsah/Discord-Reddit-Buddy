from helper_functions import reddit_helpers as rh
from helper_functions import discord_helpers as dh
from helper_functions import db_access as db


class Standard(dh.commands.Cog):
    reddit = rh.reddit_auth()

    def __intit__(self, bot):
        self.bot = bot

    @dh.commands.command(pass_context=True)
    async def hot(self, ctx, subreddit_name, num=5):
        settings = db.get_settings(ctx.guild.id)

        if num < settings[0][1]:
            subreddit = self.reddit.subreddit(subreddit_name)
            # get get [num] posts from [hot] on [subreddit]
            hot_list = rh.get_nonsticky_submissions(subreddit, "hot", num)
            await dh.post_links(ctx, hot_list)
        else:
            await ctx.send(f"This server caps the number of results requested at {settings[0][1]}")

    @dh.commands.command(pass_context=True)
    async def new(self, ctx, subreddit_name, num=5):
        settings = db.get_settings(ctx.guild.id)

        if num < settings[0][1]:
            subreddit = self.reddit.subreddit(subreddit_name)
            # get get [num] posts from [new] on [subreddit]
            new_list = rh.get_nonsticky_submissions(subreddit, "new", num)
            await dh.post_links(ctx, new_list)
        else:
            await ctx.send(f"This subreddit caps the number of results reuested at {settings[0][1]}")

    @dh.commands.command(pass_context=True)
    async def top(self, ctx, subreddit_name, num=5):
        settings = db.get_settings(ctx.guild.id)

        if num < settings[0][1]:
            subreddit = self.reddit.subreddit(subreddit_name)
            # get get [num] posts from [top] on [subreddit]
            top_list = rh.get_nonsticky_submissions(subreddit, "top", num)
            await dh.post_links(ctx, top_list)
        else:
            await ctx.send(f"This subreddit caps the number of results reuested at {settings[0][1]}")

    @dh.commands.command(pass_context=True)
    async def controversial(self, ctx, subreddit_name, num=5):
        settings = db.get_settings(ctx.guild.id)

        if num < settings[0][1]:
            subreddit = self.reddit.subreddit(subreddit_name)
            # get get [num] posts from [top] on [subreddit]
            cont_list = rh.get_nonsticky_submissions(
                subreddit, "controversial", num)
            await dh.post_links(ctx, cont_list)
        else:
            await ctx.send(f"This subreddit caps the number of results reuested at {settings[0][1]}")

    @dh.commands.command(pass_context=True)
    async def random(self, ctx, subreddit_name):
        subreddit = self.reddit.subreddit(subreddit_name)
        rand_post = subreddit.random()
        await ctx.send(rand_post.title + "\n" + rand_post.url)


def setup(bot):
    bot.add_cog(Standard(bot))
    print("Cog Loaded: Standard")
