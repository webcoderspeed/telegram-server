from telethon import TelegramClient, types
from telethon.tl.functions.messages import ExportChatInviteRequest
import time


def get_peer_type(result):
    if isinstance(result.peer_id, types.PeerChannel):
        return {
            'id': result.id,
            'peer_id': {
                'channel_id': result.peer_id.channel_id
                    },
            'date': result.date.isoformat(),
            'message': result.message,
            'out': result.out,
            'mentioned': result.mentioned,
            'media_unread': result.media_unread
        }
    elif isinstance(result.peer_id, types.PeerChat):
        return {
            'id': result.id,
            'peer_id': {
                'chat_id': result.peer_id.chat_id
                    },
            'date': result.date.isoformat(),
            'message': result.message,
            'out': result.out,
            'mentioned': result.mentioned,
            'media_unread': result.media_unread
        }
    elif isinstance(result.peer_id, types.PeerUser):
        return {
            'id': result.id,
            'peer_id': {
                'user_id': result.peer_id.user_id
                    },
            'date': result.date.isoformat(),
            'message': result.message,
            'out': result.out,
            'mentioned': result.mentioned,
            'media_unread': result.media_unread
        }
    else:
        return 'Unknown'

class TelegramLogics:
    def __init__(self, client: TelegramClient):
        self.client = client


    async def send_message(self, phone: str, message: str):
        result = await self.client.send_message(phone, message)
        result_dict = get_peer_type(result=result)
        return result_dict
        
    async def create_invite_link(self, group_link:str, expire_date= int(time.time()) + (24 * 60 * 60), usage_limit=1):
        result = await self.client(ExportChatInviteRequest(
                    peer=group_link,
                    expire_date=expire_date,  # Expiry in seconds (24 hours)
                    usage_limit=usage_limit  # Limiting to 1 member
                ))
        return result
        

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
                "id": entity.id,
                "title": entity.title
            }
        elif isinstance(entity, types.Channel):
            entity_dict = {
                "id": entity.id,
                "title": entity.title,
            }
        elif isinstance(entity, types.Group):
            entity_dict = {
                "id": entity.id,
                "title": entity.title,
            }
        else:
            raise ValueError("Unsupported entity type")

        return entity_dict
