import aiosqlite
import discord


async def add_user(database_connection: aiosqlite.Connection, database_cursor: aiosqlite.Cursor, user: int | discord.User) -> None:
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

    Returns
    -------
    A new row of data in the database.
    """
    await database_cursor.execute('INSERT INTO economy (user_id) VALUES (:user_id)', {'user_id': user})
    await database_cursor.execute('INSERT INTO animals (user_id) VALUES (:user_id)', {'user_id': user})
    await database_cursor.execute('INSERT INTO weapons (user_id) VALUES (:user_id)', {'user_id': user})
    await database_connection.commit()


async def fetch_user_economy(database_cursor: aiosqlite.Cursor, user: int | discord.User) -> aiosqlite.Row | None:
    """
    Function used by `user_is_known` to check the existence of a user in the database.

    DO NOT USE
    ----------
    """
    await database_cursor.execute('SELECT user_id FROM economy WHERE user_id = :user_id', {'user_id': user})
    output = await database_cursor.fetchone()
    return output[0] if output is not None else output


async def fetch_user_animals(database_cursor: aiosqlite.Cursor, user: int | discord.User) -> aiosqlite.Row | None:
    """
    Function used by `user_is_known` to check the existence of a user in the database.

    DO NOT USE
    ----------
    """
    await database_cursor.execute('SELECT user_id FROM animals WHERE user_id = :user_id', {'user_id': user})
    output = await database_cursor.fetchone()
    return output[0] if output is not None else output


async def fetch_user_weapons(database_cursor: aiosqlite.Cursor, user: int | discord.User) -> aiosqlite.Row | None:
    """
    Function used by `user_is_known` to check the existence of a user in the database.

    DO NOT USE
    ----------
    """
    await database_cursor.execute('SELECT user_id FROM weapons WHERE user_id = :user_id', {'user_id': user})
    output = await database_cursor.fetchone()
    return output[0] if output is not None else output


async def user_is_known(database_cursor: aiosqlite.Cursor, user: int | discord.User) -> bool:
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
    economy = await fetch_user_economy(database_cursor, user)
    animals = await fetch_user_animals(database_cursor, user)
    weapons = await fetch_user_weapons(database_cursor, user)
    return all(x == user for x in (economy, animals, weapons))


async def fetch_wallet(database_cursor: aiosqlite.Cursor, user: int | discord.User) -> int | aiosqlite.Row:
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
    await database_cursor.execute('SELECT wallet FROM economy WHERE user_id = :user_id',
                                  {'user_id': user})
    return (await database_cursor.fetchone())[0]


async def fetch_bank(database_cursor: aiosqlite.Cursor, user: int | discord.User) -> int | aiosqlite.Row:
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
    await database_cursor.execute('SELECT bank FROM economy WHERE user_id = :user_id',
                                  {'user_id': user})
    return (await database_cursor.fetchone())[0]


async def delete_user(database_connection: aiosqlite.Connection, database_cursor: aiosqlite.Cursor, user: int | discord.User) -> None:
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
    await database_cursor.execute('DELETE from economy WHERE user_id = :user_id', {'user_id': user})
    await database_cursor.execute('DELETE from animals WHERE user_id = :user_id', {'user_id': user})
    await database_cursor.execute('DELETE from weapons WHERE user_id = :user_id', {'user_id': user})
    await database_connection.commit()


async def update_wallet(database_connection: aiosqlite.Connection, database_cursor: aiosqlite.Cursor, user: int | discord.User, wallet: int = 0) -> None:
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
    await database_cursor.execute('UPDATE economy SET wallet = :wallet WHERE user_id = :user_id', {'user_id': user, 'wallet': wallet})
    await database_connection.commit()


async def update_bank(database_connection: aiosqlite.Connection, database_cursor: aiosqlite.Cursor, user: int | discord.User, bank: int = 0) -> None:
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
    await database_cursor.execute('UPDATE economy SET bank = :bank WHERE user_id = :user_id', {'user_id': user, 'bank': bank})
    await database_connection.commit()
