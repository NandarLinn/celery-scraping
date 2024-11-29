# tasks.py
from celery import Celery, Task
import requests
from sqlalchemy.exc import SQLAlchemyError
from models import SessionLocal, Post, init_db
import logging

# Initialize the database
init_db()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Celery
app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',   # Redis broker
    backend='redis://localhost:6379/0'   # Redis backend
)

# Custom base task with retry mechanism
class BaseTaskWithRetry(Task):
    autoretry_for = (requests.RequestException, SQLAlchemyError)
    retry_kwargs = {'max_retries': 3, 'countdown': 5}
    retry_backoff = True
    retry_jitter = True

# Define the Celery task
@app.task(bind=True, base=BaseTaskWithRetry)
def fetch_and_store_posts(self):
    api_url = "https://jsonplaceholder.typicode.com/posts"
    try:
        logger.info(f"Fetching data from {api_url}")
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors

        posts_data = response.json()
        if not isinstance(posts_data, list):
            raise ValueError("API response is not a list.")

        session = SessionLocal()
        logger.info(f"Processing {len(posts_data)} posts.")

        for post in posts_data:
            # Validate required fields
            if 'userId' in post and 'id' in post and 'title' in post and 'body' in post:
                # Check if post already exists to prevent duplicates
                existing_post = session.query(Post).filter_by(id=post['id']).first()
                if not existing_post:
                    new_post = Post(
                        id=post['id'],
                        user_id=post['userId'],
                        title=post['title'],
                        body=post['body']
                    )
                    session.add(new_post)
                    logger.debug(f"Added post ID {post['id']}")
                else:
                    logger.debug(f"Post ID {post['id']} already exists. Skipping.")
            else:
                logger.warning(f"Incomplete post data: {post}")

        session.commit()
        logger.info("All posts have been stored successfully.")

    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")
        raise self.retry(exc=e)

    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        raise self.retry(exc=e)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        # Do not retry for unexpected errors

    finally:
        # Ensure the session is closed
        try:
            session.close()
        except:
            pass