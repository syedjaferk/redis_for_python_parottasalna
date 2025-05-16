from celery import Celery
import time

# Set up Celery app
celery_app = Celery(
    "email_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery_app.task
def send_welcome_email(user_email: str):
    print(f"Sending welcome email to {user_email}...")
    time.sleep(3)  # Simulate time taken to send email
    print(f"Welcome email sent to {user_email}!")
    return f"Email sent to {user_email}"