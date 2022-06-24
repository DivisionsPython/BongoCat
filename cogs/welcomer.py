import discord
import os
from discord import ButtonStyle, TextChannel
from discord.ext import commands
from discord.ui import Button, View
from utils.subclasses import PrivateView, ClassicEmbed, ErrorEmbed, SuccessEmbed, WarningEmbed
from utils.welcomer_functions import fetch_background, update_background, delete_welcome_channel, set_welcome_channel, guild_is_known, fetch_channel, update_welcome_channel
from easy_pil import Editor, load_image_async, Font


class Welcomer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["setwelcome", "welcomer", "welc"])
    async def welcome(self, ctx, channel: discord.TextChannel = None):
        cursor = await self.bot.connection.cursor()
        error = ErrorEmbed()
        success = SuccessEmbed()
        if channel == None and await guild_is_known(cursor, ctx.guild.id):
            channel_id = await fetch_channel(cursor, ctx.guild.id)
            success.title = 'Welcome message already set'
            success.add_field(name="Channel", value=f'<#{str(channel_id)}>')
            await ctx.channel.send(embed=success)
        elif channel == None:
            error.title = "\u26d4 No channel provided"
            await ctx.channel.send(embed=error)
        else:
            if await guild_is_known(cursor, ctx.guild.id):
                channel_id = await fetch_channel(cursor, ctx.guild.id)
                error.title = "\u26d4 There's a welcome channel already"
                error.add_field(
                    name="Channel", value=f'<#{str(channel_id)}>', inline=True)
                error.add_field(
                    name="Maybe...", value="You wanted to update it?", inline=True)
                await ctx.channel.send(embed=error)
            else:
                await set_welcome_channel(self.bot.connection, ctx.guild.id, channel.id)
                success.title = "\u2705 Welcome channel set"
                await ctx.channel.send(embed=success)

            await cursor.close()

    @commands.command(aliases=["deletewelcome", "nowelcome"])
    async def removewelcome(self, ctx):
        cursor = await self.bot.connection.cursor()
        if await guild_is_known(cursor, ctx.guild.id):
            buttonY = Button(label='Confirm', style=ButtonStyle.green)
            buttonN = Button(label='Cancel', style=ButtonStyle.red)
            view = PrivateView(ctx.author)

            async def view_timeout():
                embed = ErrorEmbed()
                embed.title = "\u26d4 Time's up. No decision has been taken."
                await embedToEdit.edit(embed=embed, view=None)

            async def conf_callback(interaction):
                await delete_welcome_channel(self.bot.connection, ctx.guild.id)

                embed = SuccessEmbed()
                embed.title = f"\u2705 Welcome message removed"
                await embedToEdit.edit(embed=embed)

                await interaction.response.edit_message(embed=embed, view=None)

                view.stop()

            async def den_callback(interaction):
                embed = SuccessEmbed()
                embed.title = f"\u2705 Event cancelled"
                await embedToEdit.edit(embed=embed)

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
            embed = ErrorEmbed()
            embed.title = "\u26d4 No welcome channel is set"
            await ctx.channel.send(embed=embed)

        await cursor.close()

    @welcome.error
    async def wrong_channel(self, ctx, error):
        if isinstance(error, commands.ChannelNotFound):
            embed = ErrorEmbed()
            embed.title = "\u26d4 That's not a text channel"
            return await ctx.channel.send(embed=embed)

    @commands.command(aliases=["setbackground", "bg", "setbg", "newbg", "newbackground", "updatebackground", "updatebg"])
    async def background(self, ctx, background: int = None):
        cursor = await self.bot.connection.cursor()

        dir = './utils/img/bg'
        bg_length = len([name for name in os.listdir(
            dir) if os.path.isfile(os.path.join(dir, name))])

        success = SuccessEmbed()

        if background == None:
            current_bg = await fetch_background(cursor, ctx.guild.id)
            embed = ClassicEmbed()
            embed.title = f"Current backgound index set to {current_bg}"
            embed.add_field(name="Do you want to change it?",
                            value="Take a look to the list of backgrounds:")

            for times in range(bg_length):
                url = f"https://raw.githubusercontent.com/madkarmaa/BongoCat/main/utils/img/bg/{times+1}.jpg"
                embed.add_field(
                    name=f"Background {times + 1}", value=f"[Click here]({url})", inline=False)

            await ctx.channel.send(embed=embed)
        else:
            if background > (bg_length + 1) or background == 0:
                embed = ErrorEmbed()
                embed.title = "\u26d4 That's not a valid background number"
                await ctx.channel.send(embed=embed)
            else:
                try:
                    await update_background(self.bot.connection, ctx.guild.id, background)
                    current_bg = await fetch_background(cursor, ctx.guild.id)

                    success.title = f"\u2705 New background index set to {current_bg}"
                    await ctx.channel.send(embed=success)
                except:
                    embed = ErrorEmbed()
                    embed.title = "\u26d4 Unexpected error"
                    await ctx.channel.send(embed=embed)

        await cursor.close()

    @background.error
    async def bg_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = ErrorEmbed()
            embed.title = "\u26d4 That's not a valid background number"
            return await ctx.channel.send(embed=embed)
        if isinstance(error, commands.MissingPermissions):
            embed = ErrorEmbed()
            embed.title = "\u26d4 You don't have the perms to change the background"
            return await ctx.channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        cursor = await self.bot.connection.cursor()
        if await guild_is_known(cursor, member.guild.id):
            bg = await fetch_background(cursor, member.guild.id)
            channelID = await fetch_channel(cursor, member.guild.id)
            channel = self.bot.get_channel(channelID)

            background = Editor(f"./utils/img/bg/{bg}.jpg")
            pfp = await load_image_async(str(member.avatar.url))
            profile = Editor(pfp).resize((420, 420)).circle_image()

            poppins = Font.poppins(size=130, variant='bold')
            poppins_small = Font.poppins(size=75, variant='bold')

            background.paste(profile, (750, 330))
            background.ellipse((750, 330), 420, 420,
                               outline='white', stroke_width=7)

            background.text(
                (960, 120), f"WELCOME TO {member.guild.name}", color='white', font=poppins, align='center')
            background.text((960, 850), f"{member.name}#{member.discriminator}",
                            color='white', font=poppins_small, align='center')

            welcome_img = discord.File(
                fp=background.image_bytes, filename="welcome.jpg")
            await channel.send(f"{member.mention}", file=welcome_img)


async def setup(bot):
    await bot.add_cog(Welcomer(bot))
