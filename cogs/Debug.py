from helper_functions import reddit_helpers as rh
from helper_functions import discord_helpers as dh
from datetime import datetime


class Debug(dh.commands.Cog):
    reddit = rh.reddit_auth()

    def __intit__(self, bot):
        self.bot = bot

    # check that bot responds to stimulus
    @dh.commands.command(pass_context=True, hidden=True)
    async def ping(self, ctx):
        await ctx.send("pong!")

    # get the ID of the server that command was called from
    @dh.commands.command(pass_context=True, hidden=True)
    async def server_id(self, ctx):
        await ctx.send(ctx.guild.id)

    # dump database to chat - for security, only I can access full database
    @dh.commands.command(pass_context=True, hidden=True)
    async def database_dump(self, ctx):
        if (ctx.message.author.id == 230723477630353408):
            await dh.output_db(ctx)
        else:
            await dh.access_warning(ctx)

    # simulate attempted db access from someone other than myself
    @dh.commands.command(pass_context=True, hidden=True)
    async def access_fail_test(self, ctx):
        await dh.access_warning(ctx)


def setup(bot):
    bot.add_cog(Debug(bot))
    print("Cog Loaded: Debug")
