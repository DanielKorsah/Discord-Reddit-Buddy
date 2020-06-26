from helper_functions import reddit_helpers as rh
from helper_functions import discord_helpers as dh
from helper_functions import db_access as db


class Settings(dh.commands.Cog):
    def __intit__(self, bot):
        self.bot = bot

    # initialise default settings (5, 1)

    @dh.commands.Cog.listener()
    async def on_guild_join(self, guild):
        db.add_settings(guild.id, 5, 20, True)
        print(f"New server: {guild.id} with settings" +
              str(db.get_settings(guild.id)[0]))

    @dh.commands.command(pass_context=True)
    async def change_all_settings(self, ctx, default_results_length, max_results_length, nsfw):
        db.add_settings(ctx.guild.id, default_results_length,
                        max_results_length, nsfw)
        await ctx.send(f"New settings: {db.get_settings(ctx.guild.id)[0]}")

    @dh.commands.command(pass_context=True)
    async def get_settings(self, ctx):
        await ctx.send(db.get_settings(ctx.guild.id)[0])

    @dh.commands.command(pass_context=True)
    async def toggle_nsfw(self, ctx):
        length, max_length, nsfw = db.get_settings(ctx.guild.id)[0]
        nsfw = not nsfw
        db.add_settings(ctx.guild.id, length, max_length, nsfw)
        await ctx.send(f"NSFW Restricted: {bool(db.get_settings(ctx.guild.id)[0][2])}")

    @dh.commands.command(pass_context=True)
    async def set_max_results(self, ctx, maximum_results):
        db.set_max_results(ctx.guild.id, maximum_results)
        await ctx.send(f"New max results set: {db.get_settings(ctx.guild.id)[0][1]}")

    @dh.commands.command(pass_context=True)
    async def set_default_results(self, ctx, default_results_number):
        db.set_default_results(ctx.guild.id, default_results_number)
        await ctx.send(f"New default results length set: {db.get_settings(ctx.guild.id)[0][0]}")


def setup(bot):
    bot.add_cog(Settings(bot))
    print("Cog Loaded: Settings")
