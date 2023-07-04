from fastapi import APIRouter, Body, Depends
from telethon.sync import TelegramClient, events
from configparser import ConfigParser
from app.api.telegram_logics import TelegramLogics
from app.api.validators import validate_send_message
import json
from fastapi.encoders import jsonable_encoder

router = APIRouter()
config = ConfigParser()
config.read("telethon_config.ini")

api_id = config.getint("Telegram", "api_id")
api_hash = config.get("Telegram", "api_hash")
session_name = config.get("Telegram", "session_name")
phone = config.get("Telegram", "phone")

# Initialize the Telegram client
client = TelegramClient(session_name, api_id, api_hash)

# Create an instance of TelegramActions
telegram_logics = TelegramLogics(client)

@router.on_event("startup")
async def startup_event():
    global client
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        await client.sign_in(phone, input('Enter the code: '))

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
async def send_message(data: dict = Depends(validate_send_message)):
    phone = data.get("phone")
    message = data.get("message")
    await telegram_logics.send_message(phone, message)
    return {"message": "Message sent"}

@router.post("/get-entity-info")
async def get_entity_info(data: dict = Body(...)):
    entity_url = data.get("entity_url")
    entity_info = await telegram_logics.get_entity_info(entity_url)
    entity_info_json = json.dumps(entity_info, ensure_ascii=False).encode("utf-8-sig").decode()
    return {"entity_info": entity_info_json}