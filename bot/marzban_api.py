import aiohttp
from config import MARZBAN_API_URL, MARZBAN_API_KEY

async def get_user_info(marzban_username):
    headers = {"Authorization": f"Bearer {MARZBAN_API_KEY}"}
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{MARZBAN_API_URL}/users/{marzban_username}", headers=headers) as resp:
            if resp.status == 200:
                return await resp.json()
            return None
