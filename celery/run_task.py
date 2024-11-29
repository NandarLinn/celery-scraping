# run_task.py
from tasks import fetch_and_store_posts

if __name__ == "__main__":
    result = fetch_and_store_posts.delay()
    print(f"Task ID: {result.id}")
    print("Task has been dispatched.")