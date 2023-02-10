## backup_jobs

This repo contains two programs:

* `backup_jobs.py` will remove jobs from the `jobs_waiting_queue` and put them into a collection of files.  Each file contains 250K jobs.
* `load_backup.py` will take the jobs in one backup file and put them into the `jobs_waiting_queue`.

Using these programs, we can reduce the size of the `jobs_waiting_queue` so that the Redis server stops crashing.


### Process

* Make sure that no processes are running that manipulate Redis (e.g. work generator and work server).  The easiest way is to just bring the entire system down *except* Redis.
* Run `backup_jobs.py`.  This will generate `backup_jobs_1.txt`, `backup_jobs_2.txt`, etc., where each file contains 250K jobs.
* Run `load_backup.py` on `backup_jobs_1.txt` to load 250K jobs.
* Monitor the system, and when the queue gets close to empty, run `load_backup_.py` on `backup_jobs_2.txt`.
* Repeat when the queue gets close to 0.
* 