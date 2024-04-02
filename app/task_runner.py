from threading import Lock
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import os

class ThreadPool:
    def __init__(self):
        tp_num_of_threads = os.getenv("TP_NUM_OF_THREADS")
        if tp_num_of_threads:
            max_workers = int(tp_num_of_threads)
        else:
            max_workers = os.cpu_count()
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.futures = []
        self.futures_lock = Lock()
        self.running = True
        self.running_lock = Lock()

    def submit(self, task, *args):
        # Check if server is shutting down
        self.running_lock.acquire()
        running = self.running
        self.running_lock.release()
        if not running:
            return -1

        # Submit task
        self.futures_lock.acquire()
        job_id = len(self.futures) + 1
        self.futures.append(self.executor.submit(task, job_id, *args))
        self.futures_lock.release()

        return job_id

    def get_job(self, index):
        self.futures_lock.acquire()
        length = len(self.futures)
        self.futures_lock.release()

        if index < 0 or length <= index:
            return "error"
        elif self.futures[index].done():
            return "done"
        else:
            return "running"

    def get_jobs(self):
        self.futures_lock.acquire()
        length = len(self.futures)
        self.futures_lock.release()

        jobs_done = []
        for i in range(length):
            jobs_done.append(self.futures[i].done())

        return jobs_done

    def shutdown(self):
        self.running_lock.acquire()
        self.running = False
        self.running_lock.release()

        self.futures_lock.acquire()
        self.executor.shutdown()
        self.futures_lock.release()
