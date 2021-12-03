from gino import Gino
from gino.schema import GinoSchemaVisitor
from data.config import POSTGRES_URI

db = Gino()


# Documentation of Gino
# http://gino.fantix.pro/en/latest/tutorials/tutorial.html

async def create_db():
    # Database connection
    await db.set_bind(POSTGRES_URI)
    db.gino: GinoSchemaVisitor

    users = db.tables.get('users')
    # Creating the Database if does not exist
    if (users is None):
        await db.gino.drop_all()
        await db.gino.create_all()
    #
    # await db.gino.drop_all()
    # await db.gino.create_all()
