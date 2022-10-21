import motor.motor_asyncio
import certifi

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db =  client.MyFastApi
async def get_db():
    db = client.MyFastApi
    return  db