import aiosqlite
import discord


async def add_user(database_connection: aiosqlite.Connection, database_cursor: aiosqlite.Cursor, user: discord.User | int, wallet: int = 0, bank: int = 0):
    await database_cursor.execute('INSERT INTO eco VALUES (:user_id, :wallet, :bank)', {'user_id': user, 'wallet': wallet, 'bank': bank})
    await database_connection.commit()


async def fetch_user(database_cursor: aiosqlite.Cursor, user: discord.User | int):
    await database_cursor.execute('SELECT user_id FROM eco WHERE user_id = :user_id', {'user_id': user})
    output = await database_cursor.fetchone()
    if output is not None:
        return output[0]
    else:
        return output


async def user_is_known(database_cursor: aiosqlite.Cursor, user: discord.User | int) -> bool:
    return await fetch_user(database_cursor, user) == user


async def fetch_wallet(database_cursor: aiosqlite.Cursor, user: discord.User | int):
    await database_cursor.execute('SELECT wallet FROM eco WHERE user_id = :user_id',
                                  {'user_id': user})
    return (await database_cursor.fetchone())[0]


async def fetch_bank(database_cursor: aiosqlite.Cursor, user: discord.User | int):
    await database_cursor.execute('SELECT bank FROM eco WHERE user_id = :user_id',
                                  {'user_id': user})
    return (await database_cursor.fetchone())[0]


async def delete_user(database_connection: aiosqlite.Connection, database_cursor: aiosqlite.Cursor, user: discord.User | int):
    await database_cursor.execute('DELETE from eco WHERE user_id = :user_id', {'user_id': user})
    await database_connection.commit()


async def update_wallet(database_connection: aiosqlite.Connection, database_cursor: aiosqlite.Cursor, user: discord.User | int, wallet: int = 0):
    await database_cursor.execute('UPDATE eco SET wallet = :wallet WHERE user_id = :user_id', {'user_id': user, 'wallet': wallet})
    await database_connection.commit()


async def update_bank(database_connection: aiosqlite.Connection, database_cursor: aiosqlite.Cursor, user: discord.User | int, bank: int = 0):
    await database_cursor.execute('UPDATE eco SET bank = :bank WHERE user_id = :user_id', {'user_id': user, 'bank': bank})
    await database_connection.commit()
