import aiosqlite
import discord


async def set_welcome_channel(database_connection: aiosqlite.Connection, database_cursor: aiosqlite.Cursor, guild: int | discord.Guild, channel: int | discord.TextChannel):
    """
    Function to add a welcome channel to the database.

    Parameters
    ----------
    database_connection: `aiosqlite.Connection`
        The connection to the database.

    database_cursor: `aiosqlite.Cursor`
        The cursor connected to the database.

    guild: `int` (`discord.Guild.id`)
        The ID of the guild to add in the database.

    channel: `int` (`discord.TextChannel.id`)
        The ID of the channel where the bot will send the welcome message.

    Returns
    -------
    A new row of data in the database.
    """
    await database_cursor.execute('INSERT INTO welcomer (guild_id, channel_id) VALUES (:guild_id, :channel_id)', {'guild_id': guild, 'channel_id': channel})
    await database_connection.commit()


async def fetch_guild(database_cursor: aiosqlite.Cursor, guild: int | discord.Guild):
    """
    Function used by `guild_is_known` to check the existence of a guild in the database.

    DO NOT USE
    ----------
    """
    await database_cursor.execute('SELECT guild_id FROM welcomer WHERE guild_id = :guild_id', {'guild_id': guild})
    output = await database_cursor.fetchone()
    if output is not None:
        return output[0]
    else:
        return output


async def guild_is_known(database_cursor: aiosqlite.Cursor, guild: int | discord.Guild) -> bool:
    """
    Function to check if a guild is present in the database.

    Parameters
    ----------
    database_cursor: `aiosqlite.Cursor`
        The cursor connected to the database.

    guild: `int` (`discord.Guild.id`)
        The ID of the guild to check if it's present in the database.

    Returns
    -------
    `bool`:

        `True`: the guild is present in the database.

        `False`: the guild is not present in the database.
    """
    return await fetch_guild(database_cursor, guild) == guild


async def fetch_channel(database_cursor: aiosqlite.Cursor, guild: int | discord.Guild):
    """
    Function to fetch a guild's welcome channel from the database.

    Parameters
    ----------
    database_cursor: `aiosqlite.Cursor`
        The cursor connected to the database.

    guild: `int` (`discord.Guild.id`)
        The ID of the guild to check in the database.

    Returns
    -------
    `int` (`discord.TextChannel.id | aiosqlite.Row`):
        The ID of the guild's welcome channel.
    """
    await database_cursor.execute('SELECT channel_id FROM welcomer WHERE guild_id = :guild_id',
                                  {'guild_id': guild})
    return (await database_cursor.fetchone())[0]


async def fetch_background(database_cursor: aiosqlite.Cursor, guild: int | discord.Guild):
    """
    Function to fetch a guild's welcome message background index from the database.

    Parameters
    ----------
    database_cursor: `aiosqlite.Cursor`
        The cursor connected to the database.

    guild: `int` (`discord.Guild.id`)
        The ID of the guild to check in the database.

    Returns
    -------
    `int` (`aiosqlite.Row`):
        The index of the guild's welcome message background.
    """
    await database_cursor.execute('SELECT background FROM welcomer WHERE guild_id = :guild_id',
                                  {'guild_id': guild})
    return (await database_cursor.fetchone())[0]


async def delete_welcome_channel(database_connection: aiosqlite.Connection, database_cursor: aiosqlite.Cursor, guild: int | discord.Guild):
    """
    Function to remove a guild from the database.

    Parameters
    ----------
    database_connection: `aiosqlite.Connection`
        The connection to the database.

    database_cursor: `aiosqlite.Cursor`
        The cursor connected to the database.

    guild: `int` (`discord.Guild.id`)
        The ID of the guild to remove from the database.

    Returns
    -------
    The deletion of a row of data from the database.
    """
    await database_cursor.execute('DELETE from welcomer WHERE guild_id = :guild_id', {'guild_id': guild})
    await database_connection.commit()


async def update_welcome_channel(database_connection: aiosqlite.Connection, database_cursor: aiosqlite.Cursor, guild: int | discord.Guild, channel: int | discord.TextChannel):
    """
    Function to update a guild's welcome channel in the database.

    Parameters
    ----------
    database_connection: `aiosqlite.Connection`
        The connection to the database.

    database_cursor: `aiosqlite.Cursor`
        The cursor connected to the database.

    guild: `int` (`discord.Guild.id`)
        The ID of the guild to check in the database.

    channel: `int` (`discord.TextChannel.id`)
        The ID of the new welcome channel.

    Returns
    -------
    An update of data in the database.
    """
    await database_cursor.execute('UPDATE welcomer SET channel_id = :channel_id WHERE guild_id = :guild_id', {'guild_id': guild, 'channel_id': channel})
    await database_connection.commit()


async def update_background(database_connection: aiosqlite.Connection, database_cursor: aiosqlite.Cursor, guild: int | discord.Guild, background: int):
    """
    Function to update a guild's welcome channel background index in the database.

    Parameters
    ----------
    database_connection: `aiosqlite.Connection`
        The connection to the database.

    database_cursor: `aiosqlite.Cursor`
        The cursor connected to the database.

    guild: `int` (`discord.Guild.id`)
        The ID of the guild to check in the database.

    background: `int`
        The new index of the guild's welcome channel background.

    Returns
    -------
    An update of data in the database.
    """
    await database_cursor.execute('UPDATE welcomer SET background = :background WHERE guild_id = :guild_id', {'guild_id': guild, 'background': background})
    await database_connection.commit()
