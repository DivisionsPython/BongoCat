async def add_user(db, user, wallet=0, bank=0):
    cursor = await db.cursor()
    await cursor.execute('INSERT INTO eco VALUES (:user_id, :wallet, :bank)', {'user_id': user, 'wallet': wallet, 'bank': bank})
    await db.commit()
    await cursor.close()


async def fetch_user(cursor,  user):
    await cursor.execute('SELECT user_id FROM eco WHERE user_id = :user_id', {'user_id': user})
    output = await cursor.fetchone()
    if output is not None:
        return output[0]
    else:
        return output


async def fetch_wallet(cursor,  user):
    await cursor.execute('SELECT wallet FROM eco WHERE user_id = :user_id',
                         {'user_id': user})
    return (await cursor.fetchone())[0]


async def fetch_bank(cursor, user):
    await cursor.execute('SELECT bank FROM eco WHERE user_id = :user_id',
                         {'user_id': user})
    return (await cursor.fetchone())[0]


async def delete_user(db, user):
    cursor = await db.cursor()
    await cursor.execute('DELETE from eco WHERE user_id = :user_id', {'user_id': user})
    await db.commit()
    await cursor.close()


async def update_wallet(db, user, wallet):
    cursor = await db.cursor()
    await cursor.execute('UPDATE eco SET wallet = :wallet WHERE user_id = :user_id', {'user_id': user, 'wallet': wallet})
    await db.commit()
    await cursor.close()


async def update_bank(db, user, bank):
    cursor = await db.cursor()
    await cursor.execute('UPDATE eco SET bank = :bank WHERE user_id = :user_id', {'user_id': user, 'bank': bank})
    await db.commit()
    await cursor.close()
