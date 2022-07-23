import aiosqlite
import discord


async def set_welcome_channel(database_connection: aiosqlite.Connection, database_cursor: aiosqlite.Cursor, guild: discord.Guild | int, channel: discord.TextChannel | int, background: int = 1):
    await database_cursor.execute('INSERT INTO welcomer VALUES (:guild_id, :channel_id, :background)', {'guild_id': guild, 'channel_id': channel, 'background': background})
    await database_connection.commit()


async def fetch_guild(database_cursor: aiosqlite.Cursor, guild: discord.Guild | int):
    await database_cursor.execute('SELECT guild_id FROM welcomer WHERE guild_id = :guild_id', {'guild_id': guild})
    output = await database_cursor.fetchone()
    if output is not None:
        return output[0]
    else:
        return output


async def guild_is_known(database_cursor: aiosqlite.Cursor, guild: discord.Guild | int) -> bool:
    return await fetch_guild(database_cursor, guild) == guild


async def fetch_channel(database_cursor: aiosqlite.Cursor, guild: discord.Guild | int):
    await database_cursor.execute('SELECT channel_id FROM welcomer WHERE guild_id = :guild_id',
                                  {'guild_id': guild})
    return (await database_cursor.fetchone())[0]


async def fetch_background(database_cursor: aiosqlite.Cursor, guild: discord.Guild | int):
    await database_cursor.execute('SELECT background FROM welcomer WHERE guild_id = :guild_id',
                                  {'guild_id': guild})
    return (await database_cursor.fetchone())[0]


async def delete_welcome_channel(database_connection: aiosqlite.Connection, database_cursor: aiosqlite.Cursor, guild: discord.Guild | int):
    await database_cursor.execute('DELETE from welcomer WHERE guild_id = :guild_id', {'guild_id': guild})
    await database_connection.commit()


async def update_welcome_channel(database_connection: aiosqlite.Connection, database_cursor: aiosqlite.Cursor, guild: discord.Guild | int, channel: discord.TextChannel | int):
    await database_cursor.execute('UPDATE welcomer SET channel_id = :channel_id WHERE guild_id = :guild_id', {'guild_id': guild, 'channel_id': channel})
    await database_connection.commit()


async def update_background(database_connection: aiosqlite.Connection, database_cursor: aiosqlite.Cursor, guild: discord.Guild | int, background: int = 1):
    await database_cursor.execute('UPDATE welcomer SET background = :background WHERE guild_id = :guild_id', {'guild_id': guild, 'background': background})
    await database_connection.commit()
