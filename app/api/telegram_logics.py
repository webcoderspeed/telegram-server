from telethon import TelegramClient, types



class TelegramLogics:
    def __init__(self, client: TelegramClient):
        self.client = client


    async def send_message(self, phone: str, message: str):
        await self.client.send_message(phone, message)

    async def get_entity_info(self, entity_url: str):
        entity = await self.client.get_entity(entity_url)
        
        if isinstance(entity, types.User):
            entity_dict = {
            "id": entity.id,
                "first_name": entity.first_name,
                "last_name": entity.last_name,
                "username": entity.username,
            }
        elif isinstance(entity, types.Chat):
            entity_dict = {
                "title": entity.title
            }
        else:
            raise ValueError("Unsupported entity type")

        return entity_dict
