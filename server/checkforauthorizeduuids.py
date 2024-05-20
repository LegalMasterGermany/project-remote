from prisma import Prisma
import asyncio

async def init_checkforvaliduuid(uuid):
    prisma = Prisma()
    await prisma.connect()
    result = await prisma.authorized_uuids.find_unique(where={
        'uuid': uuid
    })
    await prisma.disconnect()
    return result

async def main():
    result = await init_checkforvaliduuid('312cfe03-869a-45db-91e0-84bbdfde2260')
    print(result)

asyncio.run(main())
