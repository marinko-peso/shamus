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
SEC = lambda time: round(time['end'] - time['start'], 4)

TermColorMB = lambda val: TermColors.FAIL if val > 10 else TermColors.WARNING


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
    Generates expected terminal color based on the value.
    :param memory: {Dict}
    :return: {Tuple}
    """
    kilobytes = kB(memory['end'] - memory['start'])
    if kilobytes < 1024:
        return TermColors.OKGREEN, kilobytes, 'kB'

    megabytes = MB(kilobytes)
    return TermColorMB(megabytes), megabytes, 'MB'


def get_used_time(time):
    """
    Calculate time passed. Specify terminal color to use based on value.
    :param time: {Dict}
    :return: {Tuple}
    """
    time_difference = SEC(time)
    term_color = TermColors.OKGREEN
    if time_difference > 10:
        term_color = TermColors.FAIL
    elif time_difference > 5:
        term_color = TermColors.WARNING

    return term_color, time_difference


def export_results(results):
    """
    Decide on method of exporting results.
    So far only console is supported.
    """
    memory = get_used_memory(results['memory'])
    time = get_used_time(results['time'])
    console_output(results['name'], memory, time)


def console_output(name, memory, time):
    """
    :param name: {String}
    :param memory: {Tuple}
    :param time: {Tuple}
    """
    print("%s%s%s" % (TermColors.HEADER, 2 * '-', TermColors.ENDC))
    print("%sShamus analysis for %s[%s]%s:" % (TermColors.HEADER, TermColors.BOLD, name, TermColors.ENDC))

    print("%s -> Memory: %s [%s]%s" % (memory[0], memory[1], memory[2], TermColors.ENDC))
    print("%s -> Time:   %s [s]%s" % (time[0], time[1], TermColors.ENDC))

    print("%s%s%s" % (TermColors.HEADER, 2 * '-', TermColors.ENDC))
