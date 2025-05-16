import redis

# Initialize Redis connection
r = redis.Redis(host='localhost', port=6379, db=0)

TASK_QUEUE_KEY = 'task_queue'

def add_task(task):
    r.rpush(TASK_QUEUE_KEY, task)
    print(f"Added task: {task}")

def list_tasks():
    tasks = r.lrange(TASK_QUEUE_KEY, 0, -1)
    tasks = [t.decode('utf-8') for t in tasks]
    print("Current tasks:")
    for idx, task in enumerate(tasks):
        print(f"{idx}: {task}")
    return tasks

def remove_task_by_name(task_name):
    removed = r.lrem(TASK_QUEUE_KEY, 1, task_name)
    print(f"Removed {removed} occurrence(s) of '{task_name}'")

def trim_to_recent(n):
    # Keep only the last n tasks
    total = r.llen(TASK_QUEUE_KEY)
    r.ltrim(TASK_QUEUE_KEY, total - n, -1)
    print(f"Trimmed to keep only the last {n} task(s)")

def remove_task_by_index(index):
    tasks = list_tasks()
    if index < 0 or index >= len(tasks):
        print("Invalid index")
        return

    print(f"Removing task at index {index}: {tasks[index]}")
    tasks.pop(index)

    # Replace the entire list
    r.delete(TASK_QUEUE_KEY)
    if tasks:
        r.rpush(TASK_QUEUE_KEY, *tasks)

# ---- Sample usage ----

if __name__ == '__main__':
    r.delete(TASK_QUEUE_KEY)  # Clear for fresh run

    add_task("Send email")
    add_task("Process invoice")
    add_task("Backup DB")
    add_task("Send email")  # duplicate for testing LREM

    list_tasks()
    
    remove_task_by_name("Send email")
    list_tasks()

    trim_to_recent(2)
    list_tasks()

    add_task("Clean temp files")
    add_task("Generate report")
    list_tasks()

    remove_task_by_index(1)
    list_tasks()
