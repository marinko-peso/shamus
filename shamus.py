import time
import os
from functools import wraps

import psutil


class TermColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


kB = lambda bytes: round(float(bytes) / 1024, 4)
MB = lambda kbytes: round(float(kbytes) / 1024, 4)
TermColorMB = lambda val: TermColors.FAIL if val > 10 else TermColors.WARNING
SEC = lambda time: round(time['end'] - time['start'], 4)


def shamus(caller_method):
    """
    THE ALL CREEPY SHAMUS DECORATOR!
    """
    @wraps(caller_method)
    def wrapper(*args, **kwargs):
        """
        Take data before and after running caller method.
        Only then return the caller back.
        """
        start_time = time.time()
        process = psutil.Process(os.getpid())
        start_memory = process.memory_info().rss

        response = caller_method(*args, **kwargs)

        export_results({
            'name': caller_method.__name__,
            'time': {
                'start': start_time,
                'end': time.time()
            },
            'memory': {
                'start': start_memory,
                'end': process.memory_info().rss
            }
        })

        return response

    return wrapper


def get_used_memory(memory):
    """
    Returns memory difference in Mb if more then 1Mb, otherwise in kB.
    :param memory: {Dict}
    :return: {Float}
    """
    kbytes = kB(memory['end'] - memory['start'])
    if kbytes > 1024:
        mb_val = MB(kbytes)
        return (TermColorMB(mb_val), mb_val, 'MB')

    return (TermColors.OKGREEN, kbytes, 'kB')


def get_used_time(time):
    """
    :param time: {Dict}
    :return: {Float}
    """
    diff = SEC(time)
    term_color = TermColors.OKGREEN
    if diff > 5:
        term_color = TermColors.WARNING
    if diff > 10:
        term_color = TermColors.FAIL

    return (term_color, diff)


def export_results(results):
    """
    """
    memory = get_used_memory(results['memory'])
    time = get_used_time(results['time'])
    console_output(results['name'], memory, time)


def console_output(name, memory, time):
    """
    :param memory: {Tuple}
    :param time: {Tuple}
    """
    print("%s%s%s" % (TermColors.HEADER, 2 * '-', TermColors.ENDC))
    print("%sShamus analysis for %s[%s]%s:" % (TermColors.HEADER, TermColors.BOLD, name, TermColors.ENDC))
    print("%s -> Memory: %s [%s]%s" % (memory[0], memory[1], memory[2], TermColors.ENDC))
    print("%s -> Time:   %s [s]%s" % (time[0], time[1], TermColors.ENDC))
    print("%s%s%s" % (TermColors.HEADER, 2 * '-', TermColors.ENDC))
