import discord
from discord.ext import commands
from utils.subclasses import ReportButton, CustomException, ErrorEmbed, PrivateView


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog:
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
            embed.title = "\u26d4 You don't have the perms to run this command"
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

        else:  # if unhandled error, create a report message
            user = ctx.author

            view = PrivateView(user=user).add_item(
                ReportButton(user=user, ctx=ctx, error=error))

            return await ctx.channel.send(embed=ErrorEmbed(title=f'\u26d4 Unexpected error'), view=view)


async def setup(bot):
    await bot.add_cog(Errors(bot))
