import time
import os
import logging
import datetime
from functools import wraps

import psutil

from term_colors import TermColors
from warning_levels import WarningLevels
from utils import (
    levels_options_valid,
    trailing_slash,
    format_timestamp,
    log_path_valid
)


DEFAULT_OPTIONS = {
    'output_console': True,
    'output_log': False,
    'output_log_dir': '',
    'memory_warning_levels': (1, 15),
    'time_warning_levels': (2, 10)
}
MB = lambda bytes: round(float(bytes) / (1024 ** 2), 4)
SEC = lambda time: round(time['end'] - time['start'], 4)


def shamus(options={}):
    """
    First level for parameters. Requires decorator to be called as a method.
    :param options: {Dict}
    :return: wrapper decorator method.
    """
    options = validate_options(options)

    def shamus_decorator(caller_method):
        """
        THE ALL CREEPY SHAMUS DECORATOR!
        """
        @wraps(caller_method)
        def shamus_wrapper(*args, **kwargs):
            """
            Take data before and after running caller method.
            Only then return the caller back.
            """
            start_time = time.time()
            process = psutil.Process(os.getpid())
            start_memory = process.memory_info().rss

            caller_method_response = caller_method(*args, **kwargs)

            export_results({
                'name': caller_method.__name__,
                'timestamp': datetime.datetime.utcnow(),
                'options': options,
                'time': {
                    'start': start_time,
                    'end': time.time()
                },
                'memory': {
                    'start': start_memory,
                    'end': process.memory_info().rss
                }
            })

            return caller_method_response
        return shamus_wrapper
    return shamus_decorator


def validate_options(options):
    """
    Validate sent options and merge them with default options.
    If sent options are not valid kick them out.
    :param options: {Dict}
    :return: {Dict} mutated options.
    """
    if type(options) is not dict:
        options = {}

    for levels in ['memory_warning_levels', 'time_warning_levels']:
        if levels in options and not levels_options_valid(levels):
            del options[levels]

    if 'output_log_dir' in options and not log_path_valid(options['output_log_dir']):
        del options['output_log_dir']

    final_options = DEFAULT_OPTIONS.copy()
    final_options.update(options)
    return final_options


def get_used_memory(memory, options):
    """
    Returns memory difference in MB with warning level.
    :param memory: {Dict}
    :return: {Dict}
    """
    value = MB(memory['end'] - memory['start'])
    levels = options['memory_warning_levels']

    warning_level = WarningLevels.OK
    if levels[0] < value < levels[1]:
        warning_level = WarningLevels.WARNING
    elif value >= levels[1]:
        warning_level = WarningLevels.CRITICAL

    return {
        'warning_level': warning_level,
        'val': value
    }


def get_used_time(time, options):
    """
    Returns passed time in seconds together with warning level.
    :param time: {Dict}
    :return: {Dict}
    """
    value = SEC(time)
    levels = options['time_warning_levels']

    warning_level = WarningLevels.OK
    if levels[0] < value < levels[1]:
        warning_level = WarningLevels.WARNING
    elif value >= levels[1]:
        warning_level = WarningLevels.CRITICAL

    return {
        'warning_level': warning_level,
        'val': value
    }


def export_results(results):
    """
    Decide on method of exporting results based on current options.
    """
    memory = get_used_memory(results['memory'], results['options'])
    time = get_used_time(results['time'], results['options'])

    if results['options']['output_console']:
        output_console(results['name'], results['timestamp'], memory, time)

    if results['options']['output_log']:
        output_log(results['name'], results['timestamp'], results['options'], memory, time)


def output_console(name, timestamp, memory, time):
    """
    :param name: {String}
    :param timestamp: {Datetime}
    :param memory: {Dict}
    :param time: {Dict}
    """
    # Delimiter.
    print('{}--{}'.format(TermColors.HEADER, TermColors.END_C))
    # Heading.
    print('{}shamus says @({}) for {}[{}]{}'.format(
        TermColors.HEADER,
        format_timestamp(timestamp),
        TermColors.BOLD,
        name,
        TermColors.END_C)
    )
    # Memory.
    print('{} -> Memory: {} [MB]{}'.format(
        WarningLevels.term_color(memory['warning_level']), memory['val'], TermColors.END_C)
    )
    # Time.
    print('{} -> Time:   {} [s]{}'.format(
        WarningLevels.term_color(time['warning_level']),
        time['val'],
        TermColors.END_C)
    )
    # Delimiter.
    print('{}--{}'.format(TermColors.HEADER, TermColors.END_C))


def output_log(name, timestamp, options, memory, time):
    """
    Dynamic logging level based on calculated warning level.
    :param name: {String}
    :param timestamp: {Datetime}
    :param options: {Dict}
    :param memory: {Dict}
    :param time: {Dict}
    """
    log_name = '{}shamus_{}.log'.format(
        trailing_slash(options['output_log_dir']),
        name
    )
    logging.basicConfig(filename=log_name, level=logging.INFO)

    # Timestamp logger.
    logging.info('shamus timestamp: {}'.format(format_timestamp(timestamp)))

    # Memory logger.
    mem_logger = getattr(logging, WarningLevels.logger_method(memory['warning_level']))
    mem_logger('Memory: {} [MB]'.format(memory['val']))

    # Time logger.
    time_logger = getattr(logging, WarningLevels.logger_method(time['warning_level']))
    time_logger('Time: {} [s]\n'.format(time['val']))
