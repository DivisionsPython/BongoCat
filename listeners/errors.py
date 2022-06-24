from discord.ext import commands
import traceback
from utils.subclasses import ErrorEmbed, ErrorReportEmbed


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        error = getattr(error, 'original', error)

        if isinstance(error, commands.CommandNotFound):
            embed = ErrorEmbed()
            embed.title = f'\u26d4 {error}'
            return await ctx.channel.send(embed=embed)
        if isinstance(error, commands.MemberNotFound):
            embed = ErrorEmbed()
            embed.title = f'\u26d4 {error}'
            return await ctx.channel.send(embed=embed)

        else:
            exception_list = traceback.format_exception(
                type(error), error, error.__traceback__)
            await ctx.channel.send(f'''
Exception in command **`{ctx.command}`**:
```
{"".join(exception_list)}
```
''')


async def setup(bot):
    await bot.add_cog(Errors(bot))
