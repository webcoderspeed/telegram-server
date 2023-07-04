from fastapi import Body 
from pydantic import BaseModel, validator
from fastapi.exceptions import HTTPException

def validate_send_message(data: dict = Body(...)):
  phone = data.get("phone")
  message = data.get("message")
  
  print(phone, message)
  
  if not phone:
      raise HTTPException(status_code=400, detail="Phone field is required")
  
  if not message:
      raise HTTPException(status_code=400, detail="Message field is required")
  
  return data