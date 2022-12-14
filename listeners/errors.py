from discord.ext import commands
import logging
from utils.subclasses import ReportButton, CustomException, ErrorEmbed, PrivateView, Bot
from rich.console import Console


console = Console()

try:
    log = logging.getLogger('discord')
except Exception:
    console.log(
        f'\u26d4 Failed to enable logging', style="#ff0000 bold on #ffffff")
else:
    console.log("\u2705 Logging enabled", style="#00ff00 bold")


class Errors(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if hasattr(ctx.command, 'on_error'):
            return

        if cog := ctx.cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        error = getattr(error, 'original', error)

        if isinstance(error, commands.CommandNotFound):
            pass

        elif isinstance(error, commands.MemberNotFound):
            embed = ErrorEmbed()
            embed.title = f'\u26d4 {error}'
            return await ctx.channel.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            embed = ErrorEmbed()
            embed.title = "\u26d4 You don't have the perms to run this command"
            return await ctx.channel.send(embed=embed)

        elif isinstance(error, commands.MissingRequiredArgument):
            embed = ErrorEmbed()
            embed.title = f'\u26d4 {error}'
            return await ctx.channel.send(embed=embed)

        elif isinstance(error, commands.NotOwner):
            embed = ErrorEmbed()
            embed.title = f'\u26d4 {error}'
            return await ctx.channel.send(embed=embed)

        elif isinstance(error, commands.CommandOnCooldown):
            embed = ErrorEmbed()
            embed.title = "\u26d4 Cooldown"
            embed.add_field(name='Come on bro, chill',
                            value=f"Try again in **{round(error.retry_after)}s**")
            return await ctx.channel.send(embed=embed)

        elif isinstance(error, CustomException):
            return await ctx.channel.send(embed=error.errorEmbed)

        else:  # if unhandled error, create a report message and log the error traceback
            log.log(logging.ERROR, 'Unhandled exception:', exc_info=(
                type(error), error, error.__traceback__))

            user = ctx.author

            view = PrivateView(user=user).add_item(
                ReportButton(user=user, ctx=ctx, error=error))

            return await ctx.channel.send(embed=ErrorEmbed(title=f'\u26d4 Unexpected error'), view=view)


async def setup(bot: Bot):
    await bot.add_cog(Errors(bot))
