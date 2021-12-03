from helper_functions import reddit_helpers as rh
from helper_functions import discord_helpers as dh
from helper_functions import db_access as db


class Settings(dh.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # initialise default settings (5, 20, 1)
    @dh.commands.Cog.listener()
    async def on_guild_join(self, guild):
        db.add_settings(guild.id, 5, 20, True)
        print(f"New server: {guild.id} with settings" +
              str(db.get_settings(guild.id)[0]))

    # delete server data after bot is removed or server is closed
    @dh.commands.Cog.listener()
    async def on_guild_remove(self, guild):
        db.delete_settings(guild.id)
        print(f"Server record deleted: {guild.id}")

    # change all settings for current serve at the same time
    @dh.commands.command(pass_context=True)
    @dh.discord.ext.commands.has_permissions(administrator=True)
    async def change_all_settings(self, ctx, default_results_length, max_results_length, nsfw):
        if default_results_length.isnumeric() and max_results_length.isnumeric() and nsfw.isnumeric():
            db.add_settings(ctx.guild.id, default_results_length,
                            max_results_length, nsfw)
            await ctx.send(f"New settings: {db.get_settings(ctx.guild.id)[0]}")
        else:
            await ctx.send(f"Invalid parameters: all params must be numeric. Truthiness of number is used for the boolean param.")

    # return set of settings in chat
    @dh.commands.command(pass_context=True)
    @dh.discord.ext.commands.has_permissions(administrator=True)
    async def get_settings(self, ctx):
        await ctx.send(db.get_settings(ctx.guild.id)[0])

    # toggle the nsfw_restricted settings between true and false
    @dh.commands.command(pass_context=True)
    @dh.discord.ext.commands.has_permissions(administrator=True)
    async def toggle_nsfw(self, ctx):
        length, max_length, nsfw = db.get_settings(ctx.guild.id)[0]
        nsfw = not nsfw
        db.add_settings(ctx.guild.id, length, max_length, nsfw)
        await ctx.send(f"NSFW Restricted: {bool(db.get_settings(ctx.guild.id)[0][2])}")

    # set the maximum number of results a user can request from a subreddit
    @dh.commands.command(pass_context=True)
    @dh.discord.ext.commands.has_permissions(administrator=True)
    async def set_max_results(self, ctx, maximum_results):
        if maximum_results.isnumeric():
            db.set_max_results(ctx.guild.id, maximum_results)
            await ctx.send(f"New max results set: {db.get_settings(ctx.guild.id)[0][1]}")
        else:
            await ctx.send(f"Invalid parameters: all params must be numeric.")

    # set the default number of results returned if user does not specify a number
    @dh.commands.command(pass_context=True)
    @dh.discord.ext.commands.has_permissions(administrator=True)
    async def set_default_results(self, ctx, default_results_number):
        if default_results_number.isnumeric():
            db.set_default_results(ctx.guild.id, default_results_number)
            await ctx.send(f"New default results length set: {db.get_settings(ctx.guild.id)[0][0]}")
        else:
            await ctx.send(f"Invalid parameters: all params must be numeric.")


def setup(bot):
    bot.add_cog(Settings(bot))
