async def set_welcome_channel(db, guild, channel, background=1):
    cursor = await db.cursor()
    await cursor.execute('INSERT INTO welcomer VALUES (:guild_id, :channel_id, :background)', {'guild_id': guild, 'channel_id': channel, 'background': background})
    await db.commit()
    await cursor.close()


async def fetch_guild(cursor, guild):
    await cursor.execute('SELECT guild_id FROM welcomer WHERE guild_id = :guild_id', {'guild_id': guild})
    output = await cursor.fetchone()
    if output is not None:
        return output[0]
    else:
        return output


async def guild_is_known(cursor, guild) -> bool:
    return await fetch_guild(cursor, guild) == guild


async def fetch_channel(cursor, guild):
    await cursor.execute('SELECT channel_id FROM welcomer WHERE guild_id = :guild_id',
                         {'guild_id': guild})
    return (await cursor.fetchone())[0]


async def fetch_background(cursor, guild):
    await cursor.execute('SELECT background FROM welcomer WHERE guild_id = :guild_id',
                         {'guild_id': guild})
    return (await cursor.fetchone())[0]


async def delete_welcome_channel(db, guild):
    cursor = await db.cursor()
    await cursor.execute('DELETE from welcomer WHERE guild_id = :guild_id', {'guild_id': guild})
    await db.commit()
    await cursor.close()


async def update_welcome_channel(db, guild, channel):
    cursor = await db.cursor()
    await cursor.execute('UPDATE welcomer SET channel_id = :channel_id WHERE guild_id = :guild_id', {'guild_id': guild, 'channel_id': channel})
    await db.commit()
    await cursor.close()


async def update_background(db, guild, background):
    cursor = await db.cursor()
    await cursor.execute('UPDATE welcomer SET background = :background WHERE guild_id = :guild_id', {'guild_id': guild, 'background': background})
    await db.commit()
    await cursor.close()
