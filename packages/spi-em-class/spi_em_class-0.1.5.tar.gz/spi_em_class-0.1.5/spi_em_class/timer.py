"""
Simple class for computation timing
Author: Sergey Bobkov
"""

import time

class Timer:
    """
    Timer context manager

    Example:
        with Timer() as t:
            do_smth()

        print('Time elapsed: %.03f sec.' % t.interval)

    """
    def __init__(self):
        self.start = 0
        self.end = 0
        self.interval = 0

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.interval = self.end - self.start
