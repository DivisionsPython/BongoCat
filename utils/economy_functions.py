import aiosqlite
import discord


async def add_user(database_connection: aiosqlite.Connection, database_cursor: aiosqlite.Cursor, user: discord.User | int, wallet: int = 0, bank: int = 0) -> None:
    """
    Function to add a user to the database.

    Parameters
    ----------
    database_connection: `aiosqlite.Connection`
        The connection to the database.

    database_cursor: `aiosqlite.Cursor`
        The cursor connected to the database.

    user: `int` (`discord.User.id`)
        The ID of the user to add in the database.

    wallet: `int`
        The default amount of coins a user gets in their wallet when the account is created.

        KEEP THE VALUE 0
        ----------------

    bank: `int`
        The default amount of coins a user gets in their bank when the account is created.

        KEEP THE VALUE 0
        ----------------

    Returns
    -------
    A new row of data in the database.
    """
    await database_cursor.execute('INSERT INTO eco VALUES (:user_id, :wallet, :bank)', {'user_id': user, 'wallet': wallet, 'bank': bank})
    await database_connection.commit()


async def fetch_user(database_cursor: aiosqlite.Cursor, user: discord.User | int) -> aiosqlite.Row | None:
    """
    Function used by `user_is_known` to check the existence of a user in the database.

    DO NOT USE
    ----------
    """
    await database_cursor.execute('SELECT user_id FROM eco WHERE user_id = :user_id', {'user_id': user})
    output = await database_cursor.fetchone()
    if output is not None:
        return output[0]
    else:
        return output


async def user_is_known(database_cursor: aiosqlite.Cursor, user: discord.User | int) -> bool:
    """
    Function to check if a user is present in the database.

    Parameters
    ----------
    database_cursor: `aiosqlite.Cursor`
        The cursor connected to the database.

    user: `int` (`discord.User.id`)
        The ID of the user to check if it's present in the database.

    Returns
    -------
    `bool`:

        `True`: the user is present in the database.

        `False`: the user is not present in the database.
    """
    return await fetch_user(database_cursor, user) == user


async def fetch_wallet(database_cursor: aiosqlite.Cursor, user: discord.User | int) -> int | aiosqlite.Row:
    """
    Function to fetch a user's wallet from the database.

    Parameters
    ----------
    database_cursor: `aiosqlite.Cursor`
        The cursor connected to the database.

    user: `int` (`discord.User.id`)
        The ID of the user to check in the database.

    Returns
    -------
    `int` (`aiosqlite.Row`):
        The value of the user's wallet.
    """
    await database_cursor.execute('SELECT wallet FROM eco WHERE user_id = :user_id',
                                  {'user_id': user})
    return (await database_cursor.fetchone())[0]


async def fetch_bank(database_cursor: aiosqlite.Cursor, user: discord.User | int) -> int | aiosqlite.Row:
    """
    Function to fetch a user's bank from the database.

    Parameters
    ----------
    database_cursor: `aiosqlite.Cursor`
        The cursor connected to the database.

    user: `int` (`discord.User.id`)
        The ID of the user to check in the database.

    Returns
    -------
    `int` (`aiosqlite.Row`):
        The value of the user's bank.
    """
    await database_cursor.execute('SELECT bank FROM eco WHERE user_id = :user_id',
                                  {'user_id': user})
    return (await database_cursor.fetchone())[0]


async def delete_user(database_connection: aiosqlite.Connection, database_cursor: aiosqlite.Cursor, user: discord.User | int) -> None:
    """
    Function to remove a user from the database.

    Parameters
    ----------
    database_connection: `aiosqlite.Connection`
        The connection to the database.

    database_cursor: `aiosqlite.Cursor`
        The cursor connected to the database.

    user: `int` (`discord.User.id`)
        The ID of the user to remove from the database.

    Returns
    -------
    The deletion of a row of data from the database.
    """
    await database_cursor.execute('DELETE from eco WHERE user_id = :user_id', {'user_id': user})
    await database_connection.commit()


async def update_wallet(database_connection: aiosqlite.Connection, database_cursor: aiosqlite.Cursor, user: discord.User | int, wallet: int = 0) -> None:
    """
    Function to update a user's wallet in the database.

    Parameters
    ----------
    database_connection: `aiosqlite.Connection`
        The connection to the database.

    database_cursor: `aiosqlite.Cursor`
        The cursor connected to the database.

    user: `int` (`discord.User.id`)
        The ID of the user to check in the database.

    wallet: `int`
        The amount of coins the user gets in their wallet.

    Returns
    -------
    An update of data in the database.
    """
    await database_cursor.execute('UPDATE eco SET wallet = :wallet WHERE user_id = :user_id', {'user_id': user, 'wallet': wallet})
    await database_connection.commit()


async def update_bank(database_connection: aiosqlite.Connection, database_cursor: aiosqlite.Cursor, user: discord.User | int, bank: int = 0) -> None:
    """
    Function to update a user's bank in the database.

    Parameters
    ----------
    database_connection: `aiosqlite.Connection`
        The connection to the database.

    database_cursor: `aiosqlite.Cursor`
        The cursor connected to the database.

    user: `int` (`discord.User.id`)
        The ID of the user to check in the database.

    bank: `int`
        The amount of coins the user gets in their bank.

    Returns
    -------
    An update of data in the database.
    """
    await database_cursor.execute('UPDATE eco SET bank = :bank WHERE user_id = :user_id', {'user_id': user, 'bank': bank})
    await database_connection.commit()
