from helper_functions import reddit_helpers as rh
from helper_functions import discord_helpers as dh


class Debug(dh.commands.Cog):
    reddit = rh.reddit_auth()

    def __intit__(self, bot):
        self.bot = bot

    @dh.commands.command(pass_context=True, hidden=True)
    async def ping(self, ctx):
        await ctx.send("pong!")

    @dh.commands.command(pass_context=True, hidden=True)
    async def server_id(self, ctx):
        await ctx.send(ctx.guild.id)

    # security - only I can access full database
    @dh.commands.command(pass_context=True, hidden=True)
    async def database_dump(self, ctx):
        if (ctx.message.author.id == 230723477630353408):
            await dh.output_db(ctx)
        else:
            await dh.access_warning(ctx)

    @dh.commands.command(pass_context=True, hidden=True)
    async def access_fail_test(self, ctx):
        await dh.access_warning(ctx)


def setup(bot):
    bot.add_cog(Debug(bot))
    print("Cog Loaded: Debug")
