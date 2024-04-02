Name: Barbu Sorin-Petruț \
Group: 331CC

# Homework 1

## Organization

- The core element of this homework was the ThreadPool.
- The server works like placing orders:
  - The client would request some data (e.g., states_mean).
  - A job ID would be returned (e.g., job_id_1).
  - The client would check and get the result using the job ID.
- I chose to use ThreadPoolExecutor rather than creating one from scratch.
  - Benefits:
    - Faster and more secure implementation.
    - Covers most of what I needed.
  - Cons:
    - Futures management.
- The API is developed in Flask.

**_Mandatory:_**

- The ThreadPool was based on ThreadPoolExecutor.
- For each submission, the next job ID would be retrieved from the futures array length.
- Each task function submitted to the executor receives a job ID to store the result properly.
- To check if a task/job is done, we check if the future at the right index based on the job ID is done.

## Implementation

1. submit(task, \*args)

   - Check if the server is shutting down
     ```
     self.running_lock.acquire()
     running = self.running
     self.running_lock.release()
     if not running:
         return -1
     ```
   - Generate the next job ID and submit the task to the executor(ThreadPoolExecutor)

     ```
     self.futures_lock.acquire()
     job_id = len(self.futures) + 1
     self.futures.append(self.executor.submit(task, job_id, *args))
     self.futures_lock.release()
     ```

2. get_job(index)

   - Check if the index is outside the array length and if the future is done using the built-in function done()

     ```
     self.futures_lock.acquire()
     length = len(self.futures)
     self.futures_lock.release()

     if index < 0 or length <= index:
         return "error"
     elif self.futures[index].done():
         return "done"
     else:
         return "running"
     ```

3. get_jobs()

   - Get the array length in a thread-safe way, iterate for the first length elements in the array, and generate a new array containing booleans (True => job is done, False => job is not done)

     ```
     self.futures_lock.acquire()
     length = len(self.futures)
     self.futures_lock.release()

     jobs_done = []
     for i in range(length):
       jobs_done.append(self.futures[i].done())

     return jobs_done
     ```

## Resources Used

- https://ocw.cs.pub.ro/courses/asc/laboratoare/03#threadpoolexecutor

## Git

- https://github.com/SorinBar/le_stats_sportif (Private)
