
import random
import logging
from locust import task, constant
from locust.contrib.fasthttp import FastHttpUser


log = logging.getLogger("rest-api-short-urls")
todo_ids = range(1, 200000)


class LocustClient(FastHttpUser):
    wait_time = constant(0)
    host = "http://localhost:8000/todos"


    def __init__(self, environment):
        """ Class constructor."""
        super().__init__(environment)


    @task
    def test_get_todos(self):

        try:
            url = random.choice(todo_ids)
            with self.client.get(f'/{url}', name='get todo id') as resp_of_api:
                if resp_of_api.status_code == 200:
                    log.info("API call resulted in success.")

                else:
                    log.error("API call resulted in failed.")
             
        except Exception as e:
            log.error(f"Exception occurred! details are {e}")