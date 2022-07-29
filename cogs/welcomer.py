import contextlib
import discord
import os
import dotenv
from discord import ButtonStyle, Embed, SelectOption
from discord.ext import commands
from discord.ui import Button, View
from utils.subclasses import Bot, PrivateView, ClassicEmbed, ErrorEmbed, SuccessEmbed, WarningEmbed, CustomException
from utils.welcomer_functions import fetch_background, update_background, delete_welcome_channel, set_welcome_channel, guild_is_known, fetch_channel, update_welcome_channel
from easy_pil import Editor, load_image_async, Font

PREFIX = dotenv.dotenv_values('.env')['PREFIX']
BACKGOUNDS_DIR = dotenv.dotenv_values('.env')['BACKGOUNDS_DIR']


class BgSelect(discord.ui.Select):
    bg_length = len([name for name in os.listdir(
        BACKGOUNDS_DIR) if os.path.isfile(os.path.join(BACKGOUNDS_DIR, name))])
    options = []

    for times in range(bg_length):
        options.append(
            SelectOption(
                label=f'Background {times+1}', value=f'{times+1}', description='Select to show')
        )

    def __init__(self) -> None:
        super().__init__(
            options=self.options,
            placeholder="Choose a background to show"
        )

    async def callback(self, interaction):
        for times in range(self.bg_length):
            if self.values[0] == f'{times+1}':
                embed = ClassicEmbed()
                embed.title = f'Background {times+1}'
                embed.set_image(
                    url=f"https://raw.githubusercontent.com/madkarmaa/BongoCat/main/utils/img/bg/{times+1}.jpg")
                embed.add_field(name='Is this your choice?',
                                value=f'Run the command `{PREFIX}welcome background {times+1}` or click "**Select**"')
                await interaction.response.edit_message(embed=embed)

    def get_bg_length(self) -> int:
        return self.bg_length

    def get_selector_value(self) -> int | None:
        return self.values[0] if self.values else None


class Welcomer(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.group(description="Welcome commands group.")
    @commands.has_permissions(administrator=True)
    async def welcome(self, ctx: commands.Context):
        '''Welcome commands group. Use `help welcome` for more details.'''
        if ctx.invoked_subcommand is None:
            raise CustomException("What do you want to do?")

    @welcome.command(description="Select a channel where to send the welcome message.")
    async def set(self, ctx: commands.Context, channel: discord.TextChannel = None):
        '''Set the welcome channel.'''
        success = SuccessEmbed()
        warning = WarningEmbed()
        if channel is None and await guild_is_known(self.bot.dbcursor, ctx.guild.id):
            channel_id = await fetch_channel(self.bot.dbcursor, ctx.guild.id)
            success.title = 'Welcome message already set'
            success.add_field(name="Channel", value=f'<#{str(channel_id)}>')
            await ctx.channel.send(embed=success)
        elif await guild_is_known(self.bot.dbcursor, ctx.guild.id):
            channel_id = await fetch_channel(self.bot.dbcursor, ctx.guild.id)
            warning.title = "\u26a0 There's a welcome channel already"
            warning.add_field(
                name="Channel", value=f'<#{str(channel_id)}>', inline=True)
            warning.add_field(
                name="Maybe...", value=f"You wanted to update it?\nRun the command `{PREFIX}welcome update <channel>`", inline=True)
            await ctx.channel.send(embed=warning)
        else:
            await set_welcome_channel(self.bot.dbconnection, self.bot.dbcursor, ctx.guild.id, channel.id)
            success.title = "\u2705 Welcome channel set"
            await ctx.channel.send(embed=success)

    @set.error
    async def wrong_channel(self, ctx: commands.Context, error):
        if isinstance(error, commands.ChannelNotFound):
            embed = ErrorEmbed()
            embed.title = "\u26d4 That's not a text channel"
            return await ctx.channel.send(embed=embed)

    @welcome.command(description="Update the channel where to send the welcome message.")
    async def update(self, ctx: commands.Context, channel: discord.TextChannel = None):
        '''Update the welcome channel.'''
        success = SuccessEmbed()

        if await guild_is_known(self.bot.dbcursor, ctx.guild.id):
            if await guild_is_known(self.bot.dbcursor, ctx.guild.id) and await fetch_channel(self.bot.dbcursor, ctx.guild.id) == channel.id:
                embed = WarningEmbed()
                embed.title = "\u26a0 That's the current welcome channel"
                await ctx.channel.send(embed=embed)
            else:
                await update_welcome_channel(self.bot.dbconnection, self.bot.dbcursor, ctx.guild.id, channel.id)
                channel_id = await fetch_channel(self.bot.dbcursor, ctx.guild.id)
                success.title = "\u2705 Welcome channel updated"
                success.add_field(
                    name="Channel", value=f'<#{str(channel_id)}>')
                await ctx.channel.send(embed=success)

        else:
            raise CustomException("No welcome channel is set")

    @update.error
    async def wrong_channel2(self, ctx: commands.Context, error):
        if isinstance(error, commands.ChannelNotFound):
            embed = ErrorEmbed()
            embed.title = "\u26d4 That's not a text channel"
            return await ctx.channel.send(embed=embed)

    @welcome.command(description="Remove the channel where to send the welcome message. No welcome message will be shown.")
    async def remove(self, ctx: commands.Context):
        '''Remove the welcome channel.'''
        if await guild_is_known(self.bot.dbcursor, ctx.guild.id):
            buttonY = Button(label='Confirm', style=ButtonStyle.green)
            buttonN = Button(label='Cancel', style=ButtonStyle.red)
            view = PrivateView(ctx.author)

            async def view_timeout():
                embed = ErrorEmbed()
                embed.title = "\u26d4 Time's up. No decision has been taken."
                await embedToEdit.edit(embed=embed, view=None)

            async def conf_callback(interaction):
                await delete_welcome_channel(self.bot.dbconnection, self.bot.dbcursor, ctx.guild.id)

                embed = SuccessEmbed()
                embed.title = f"\u2705 Welcome message removed"

                await interaction.response.edit_message(embed=embed, view=None)

                view.stop()

            async def den_callback(interaction):
                embed = SuccessEmbed()
                embed.title = f"\u2705 Event cancelled"

                await interaction.response.edit_message(embed=embed, view=None)

                view.stop()

            buttonN.callback = den_callback
            buttonY.callback = conf_callback
            view.add_item(buttonY)
            view.add_item(buttonN)

            embed = WarningEmbed()
            embed.title = "\u26a0 Do you really want to remove the welcome message?"
            embed.add_field(name="You still have time!",
                            value="You have **60** seconds to confirm/cancel.")
            embedToEdit = await ctx.channel.send(embed=embed, view=view)

            view.on_timeout = view_timeout
        else:
            raise CustomException("No welcome channel is set")

    @welcome.command(aliases=["bg"], description="Update the background for the welcome message. Select from the options.")
    async def background(self, ctx: commands.Context, background: int = None):
        '''Update the background for the welcome message.'''
        if await guild_is_known(self.bot.dbcursor, ctx.guild.id):
            if background == None:
                current_bg = await fetch_background(self.bot.dbcursor, ctx.guild.id)
                buttonY = Button(label='Select', style=ButtonStyle.green)
                buttonN = Button(label='Exit', style=ButtonStyle.red)
                selector = BgSelect()

                async def set_callback(interaction):
                    success = SuccessEmbed()
                    error = ErrorEmbed()
                    bg_value = selector.get_selector_value()

                    if bg_value is not None:
                        try:
                            await update_background(self.bot.dbconnection, self.bot.dbcursor, ctx.guild.id, bg_value)
                            current_bg = await fetch_background(self.bot.dbcursor, ctx.guild.id)
                            success.title = f"\u2705 New background index set to {current_bg}"

                            await interaction.response.edit_message(embed=success, view=None)
                            view.stop()
                        except:
                            raise CustomException
                    else:
                        error.title = "\u26d4 No background has been selected"
                        await interaction.response.send_message(embed=error)

                async def exit_callback(interaction):
                    await interaction.response.edit_message(view=None)
                    view.stop()

                embed = ClassicEmbed()
                embed.title = f"Current backgound index set to {current_bg}"
                embed.add_field(name="Do you want to change it?",
                                value="Take a look to the list of backgrounds")

                buttonN.callback = exit_callback
                buttonY.callback = set_callback

                view = PrivateView(ctx.author, timeout=180)
                view.add_item(selector)
                view.add_item(buttonY)
                view.add_item(buttonN)

                await ctx.channel.send(embed=embed, view=view)
            else:
                selector = BgSelect()
                bg_length = selector.get_bg_length()
                if background > (bg_length + 1) or background == 0:
                    embed = ErrorEmbed()
                    embed.title = "\u26d4 That's not a valid background number"
                    await ctx.channel.send(embed=embed)

        else:
            raise CustomException("There's no welcome channel set")

    @background.error
    async def bg_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.BadArgument):
            embed = ErrorEmbed()
            embed.title = "\u26d4 That's not a valid background number"
            return await ctx.channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member | discord.User):
        if not await guild_is_known(self.bot.dbcursor, member.guild.id):
            return
        bg = await fetch_background(self.bot.dbcursor, member.guild.id)
        channelID = await fetch_channel(self.bot.dbcursor, member.guild.id)
        channel = self.bot.get_channel(channelID)
        server_name = str(member.guild.name)

        background = Editor(f"./utils/img/bg/{bg}.jpg")
        pfp = await load_image_async(str(member.avatar.url))
        profile = Editor(pfp).resize((420, 420)).circle_image()

        if len(member.guild.name) <= 20:
            guild_name_font_size = 130
            guild_name_font_outline_size = 132
        elif 20 < len(member.guild.name) <= 25:
            guild_name_font_size = 120
            guild_name_font_outline_size = 122
        else:
            guild_name_font_size = 130
            guild_name_font_outline_size = 132
            server_name = "This server"

        poppins = Font.poppins(size=guild_name_font_size, variant='bold')
        poppins_outline = Font.poppins(
            size=guild_name_font_outline_size, variant='bold')
        poppins_small = Font.poppins(size=75, variant='bold')
        poppins_small_outline = Font.poppins(size=76, variant='bold')

        background.paste(profile, (750, 330))
        background.ellipse((750, 330), 420, 420,
                           outline='white', stroke_width=7)

        background.text(
            (960, 54), "Welcome to", color='black', font=poppins_small_outline, align='center')
        background.text(
            (960, 50), "Welcome to", color='white', font=poppins_small, align='center')

        background.text(
            (960, 164), server_name, color='black', font=poppins_outline, align='center')
        background.text(
            (960, 160), server_name, color='white', font=poppins, align='center')

        background.text((960, 854), f"{member.name}#{member.discriminator}",
                        color='black', font=poppins_small_outline, align='center')
        background.text((960, 850), f"{member.name}#{member.discriminator}",
                        color='white', font=poppins_small, align='center')

        welcome_img = discord.File(
            fp=background.image_bytes, filename="welcome.jpg")
        try:
            await channel.send(f"{member.mention}", file=welcome_img)
        except AttributeError:
            with contextlib.suppress(Exception):
                embed = ErrorEmbed()
                embed.title = "\u26d4 The welcome channel was not found in the server."
                await member.guild.system_channel.send(embed=embed)


async def setup(bot: Bot):
    await bot.add_cog(Welcomer(bot))
