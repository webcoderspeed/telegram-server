from fastapi import APIRouter, Body
from telethon.sync import TelegramClient
from configparser import ConfigParser
from app.api.telegram_logics import TelegramLogics
import json
from telethon.errors import SessionPasswordNeededError

router = APIRouter()
config = ConfigParser()
config.read("telethon_config.ini")

api_id = config.getint("Telegram", "api_id")
api_hash = config.get("Telegram", "api_hash")
session_name = config.get("Telegram", "session_name")
phone = config.get("Telegram", "phone")
password = config.get("Telegram", "password")

# Initialize the Telegram client
client = TelegramClient(session_name, api_id, api_hash)

# Create an instance of TelegramActions
telegram_logics = TelegramLogics(client)

@router.on_event("startup")
async def startup_event():
    global client
    await client.connect()
    if not await client.is_user_authorized():
        try:
            await client.send_code_request(phone)
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=password)

        # Print the logged-in user details
        me = await client.get_me()
        print('You are now logged in as', me.first_name)


@router.on_event("shutdown")
async def shutdown_event():
    global client
    await client.disconnect()
    

@router.get('/')
async def health_check():
    return {"message": "server is running..."}


@router.post("/send-message")
async def send_message(data: dict = Body(...)):
    phone = data.get("phone")
    message = data.get("message")
    result = await telegram_logics.send_message(phone, message)
    response_json = json.dumps(result)
    return {"result": response_json}

@router.post("/get-entity-info")
async def get_entity_info(data: dict = Body(...)):
    try:
        entity_url = data.get("entity_url")
        entity_info = await telegram_logics.get_entity_info(entity_url)
        entity_info_json = json.dumps(entity_info)
        return {"entity_info": entity_info_json}
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {"error": str(e)}

@router.post("/create-invite-link")
async def create_invite_link(data: dict = Body(...)):
    group_link = data.get("group_link")
    expire_date = data.get("expire_date")
    usage_limit = data.get("usage_limit")
    invite_link = await telegram_logics.create_invite_link(group_link, expire_date, usage_limit)
    return {"invite_link": invite_link.link}
