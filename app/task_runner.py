from threading import Lock
from concurrent.futures import ThreadPoolExecutor
from enum import Enum

class ThreadPool:
    def __init__(self):
        # You must implement a ThreadPool of TaskRunners
        # Your ThreadPool should check if an environment variable TP_NUM_OF_THREADS is defined
        # If the env var is defined, that is the number of threads to be used by the thread pool
        # Otherwise, you are to use what the hardware concurrency allows
        # You are free to write your implementation as you see fit, but
        # You must NOT:
        #   * create more threads than the hardware concurrency allows
        #   * recreate threads for each task

        # TODO get max_workers
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.futures = []
        self.lock = Lock()
    
    def submit(self, task, *args):
        self.lock.acquire()
        job_id = len(self.futures) + 1
        self.futures.append(self.executor.submit(task, job_id, *args))
        self.lock.release()

        return job_id

    def get_job(self, index):
        self.lock.acquire()
        length = len(self.futures)
        self.lock.release()

        if index < 0 or length <= index:
            return "error"
        elif self.futures[index].done():
            return "done"
        else:
            return "running"

    def get_jobs(self):
        self.lock.acquire()
        length = len(self.futures)
        self.lock.release()

        for i in range(length):
            print(i, end=' ')
            print(self.futures[i].done())
        
   


    def shutdown(self):
        self.executor.shutdown()