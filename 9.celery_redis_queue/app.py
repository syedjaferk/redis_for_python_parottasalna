# main.py
from tasks import background_task

# Trigger the task asynchronously
result = background_task.delay(5)

print(f"Task submitted. Task ID: {result.id}")
