from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel, EmailStr
from app.tasks import send_welcome_email

app = FastAPI()

class User(BaseModel):
    email: EmailStr

@app.post("/register/")
def register_user(user: User):
    # Queue the background email sending task
    send_welcome_email.delay(user.email)
    return {"message": f"User {user.email} registered successfully. Email will be sent shortly."}
