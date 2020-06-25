from helper_functions import reddit_helpers as rh
from helper_functions import discord_helpers as dh
from helper_functions import db_access as db


class Debug(dh.commands.Cog):
    reddit = rh.reddit_auth()

    def __intit__(self, bot):
        self.bot = bot

    @dh.commands.command(pass_context=True, hidden=True)
    async def ping(self, ctx):
        await ctx.send("pong!")

    @dh.commands.command(pass_context=True, hidden=True)
    async def snowflake(self, ctx):
        await ctx.send(ctx.guild.id)


def setup(bot):
    bot.add_cog(Debug(bot))
    print("Cog Loaded: Debug")
