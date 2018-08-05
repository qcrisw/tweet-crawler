import os

from redis import Redis
from rq import Queue

class TaskQueue:
    
    def __init__(self, name='default', url=os.environ['REDIS_URL']):
        self.redis = Redis.from_url(url)
        self.q = Queue(name, connection=self.redis)
    
    def add_task(self, task_func, *args, **kwargs):
        self.q.enqueue_call(task_func, args=args, kwargs=kwargs)
