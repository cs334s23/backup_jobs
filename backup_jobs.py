
from redis import Redis
import json


class BackupJobs:
    """
    This class drives a process to back up all jobs in the
    jobs_waiting_queue into a collections of files.  The files
    will be named job_backup_1.txt, job_backup_2.txt, etc., and
    each job will contain the same number of jobs (except the
    last, which will contain fewer, since the size of the queue
    isn't a multiple of the file size).
    """

    def __init__(self):
        self.r = Redis()
        self.jobs_per_file = 250000
        self.next_file_index = 1

    def get_job(self):
        """
        Remove one job from the jobs_waiting_queue, and return that
        job as a string
        """
        return json.loads(self.r.lpop('jobs_waiting_queue'))

    def get_next_filename(self):
        """
        Get the next filename, of the form job_backup_<num>.txt
        """
        index = self.next_file_index
        self.next_file_index += 1
        return 'job_backup_{}.txt'.format(index)

    def save_one_file(self):
        """
        Save jobs_per_file jobs into the next backup file.
        """
        filename = self.get_next_filename()
        print('Saving to {}'.format(filename))
        with open(filename, 'w') as out:
            # Since the number of jobs isn't a multiple of
            # jobs_per_file, the last file will have fewer lines
            num_records = min(self.jobs_per_file, self.num_jobs())
            for count in range(num_records):
                # +1 because range starts at 0
                print('\r{}'.format(count + 1), end='')
                out.write(json.dumps(self.get_job()) + '\n')
        print()

    def num_jobs(self):
        """
        Get the current number of jobs in the jobs_waiting_queue
        """
        return self.r.llen('jobs_waiting_queue')

    def db_has_more_jobs(self):
        """
        Determine if there are more jobs in the jobs_waiting_queue
        """
        return self.r.llen('jobs_waiting_queue') != 0

    def create_backup(self):
        """
        Back up all data into files.
        """
        while self.db_has_more_jobs():
            self.save_one_file()


if __name__ == '__main__':
    backup = BackupJobs()
    backup.create_backup()
