from redis import Redis
import sys


class LoadBackup:
    """
    This class drives the process to load the contents of one
    back up file into the jobs_waiting_queue
    """
    def __init__(self):
        self.r = Redis()

    def load_backup(self, filename):
        """
        Load the contents of the file into the queue
        """
        print('Loading {}'.format(filename))
        with open(filename, 'r') as file:
            count = 1
            for line in file:
                line = line.strip()
                print('\r{}'.format(count), end='')
                count += 1
                self.r.rpush('jobs_waiting_queue', line)
        print()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('ERROR: Give backup filename.')
        sys.exit(1)

    filename = sys.argv[1]
    load = LoadBackup()

    load.load_backup(filename)
