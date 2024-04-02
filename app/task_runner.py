from threading import Lock
from concurrent.futures import ThreadPoolExecutor

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
        self.executor = ThreadPoolExecutor(max_workers=10)
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
