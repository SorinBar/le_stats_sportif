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
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.futures = []
        self.lock = Lock()
    
    def submit(self, task, *args):
        self.lock.acquire()
        self.futures.append(self.executor.submit(task, args))
        self.lock.release()
    
    def get_jobs(self):
        length = 0
        self.lock.acquire()
        length = len(self.futures)
        self.lock.release()

        for i in range(length):
            print(i, end=' ')
            print(self.futures[i].done())
        
    def is_job_done(self, index):
        length = 0
        self.lock.acquire()
        length = len(self.futures)
        self.lock.release()

        if index >= length:
            return False
        else:
            return self.futures[index].done()


    def shutdown(self):
        self.executor.shutdown()