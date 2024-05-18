from prisma import Prisma

async def init_checkforvaliduuid(uuid):
    prisma = Prisma()
    await prisma.connect()
    return prisma.authorized_uuids.