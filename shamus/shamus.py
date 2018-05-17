__all__ = ['shamus']

if __name__ == '__main__':
    from term_colors import _TermColors
    print('{header}{msg}{end}'.format(
        header=_TermColors.HEADER,
        msg='shamus says: i am not supposed to be used like this!',
        end=_TermColors.END_C
    ))
    exit(0)


import time
import os
import logging
import datetime
from functools import wraps

import psutil

from .term_colors import _TermColors
from .warning_levels import _WarningLevels
from .utils import (
    _levels_options_valid,
    _trailing_slash,
    _format_timestamp,
    _log_path_valid
)


DEFAULT_OPTIONS = {
    'output_console': True,
    'output_log': False,
    'output_log_dir': '',
    'memory_warning_levels': (1, 15),
    'time_warning_levels': (2, 10)
}


def MB(bytes): return round(float(bytes) / (1024 ** 2), 4)


def SEC(time): return round(time['end'] - time['start'], 4)


def shamus(options={}):
    """
    First level for parameters. Requires decorator to be called as a method.
    :param options: {Dict}
    :return: wrapper decorator method.
    """
    options = __validate_options(options)

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

            __export_results({
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


def __validate_options(options: dict) -> dict:
    """
    Validate sent options and merge them with default options.
    If sent options are not valid kick them out.
    :param options: {Dict}
    :return: {Dict} mutated options.
    """
    if type(options) is not dict:
        options = {}

    for levels in ['memory_warning_levels', 'time_warning_levels']:
        if levels in options and not _levels_options_valid(levels):
            del options[levels]

    if 'output_log_dir' in options and not _log_path_valid(options['output_log_dir']):
        del options['output_log_dir']

    final_options = DEFAULT_OPTIONS.copy()
    final_options.update(options)
    return final_options


def __get_used_memory(memory: dict, options: dict) -> dict:
    """
    Returns memory difference in MB with warning level.
    :param memory: {Dict}
    :return: {Dict}
    """
    value = MB(memory['end'] - memory['start'])
    levels = options['memory_warning_levels']

    warning_level = _WarningLevels.OK
    if levels[0] < value < levels[1]:
        warning_level = _WarningLevels.WARNING
    elif value >= levels[1]:
        warning_level = _WarningLevels.CRITICAL

    return {
        'warning_level': warning_level,
        'val': value
    }


def __get_used_time(time: dict, options: dict) -> dict:
    """
    Returns passed time in seconds together with warning level.
    :param time: {Dict}
    :param options: {Dict}
    :return: {Dict}
    """
    value = SEC(time)
    levels = options['time_warning_levels']

    warning_level = _WarningLevels.OK
    if levels[0] < value < levels[1]:
        warning_level = _WarningLevels.WARNING
    elif value >= levels[1]:
        warning_level = _WarningLevels.CRITICAL

    return {
        'warning_level': warning_level,
        'val': value
    }


def __export_results(results: dict):
    """
    Decide on method of exporting results based on current options.
    """
    memory = __get_used_memory(results['memory'], results['options'])
    time = __get_used_time(results['time'], results['options'])

    if results['options']['output_console']:
        __output_console(results['name'], results['timestamp'], memory, time)

    if results['options']['output_log']:
        __output_log(
            results['name'],
            results['timestamp'],
            results['options'],
            memory,
            time
        )


def __output_console(name: str, timestamp: datetime, memory: dict, time: dict):
    """
    :param name: {String}
    :param timestamp: {Datetime}
    :param memory: {Dict}
    :param time: {Dict}
    """
    # Delimiter.
    print(f'{_TermColors.HEADER}--{_TermColors.END_C}')
    # Heading.
    print('{header}shamus says @({time}) for {b}[{name}]{end}'.format(
        header=_TermColors.HEADER,
        time=_format_timestamp(timestamp),
        b=_TermColors.BOLD,
        name=name,
        end=_TermColors.END_C
    ))
    # Memory.
    print('{level} -> Memory: {memory} [MB]{end}'.format(
        level=_WarningLevels.term_color(memory['warning_level']),
        memory=memory['val'],
        end=_TermColors.END_C
    ))
    # Time.
    print('{level} -> Time:   {time} [s]{end}'.format(
        level=_WarningLevels.term_color(time['warning_level']),
        time=time['val'],
        end=_TermColors.END_C
    ))
    # Delimiter.
    print(f'{_TermColors.HEADER}--{_TermColors.END_C}')


def __output_log(name: str, timestamp: datetime, options: dict, memory: dict, time: dict):
    """
    Dynamic logging level based on calculated warning level.
    :param name: {String}
    :param timestamp: {Datetime}
    :param options: {Dict}
    :param memory: {Dict}
    :param time: {Dict}
    """
    log_name = f"{_trailing_slash(options['output_log_dir'])}shamus_{name}.log"
    logging.basicConfig(filename=log_name, level=logging.INFO)

    # Timestamp logger.
    logging.info(f'shamus timestamp: {_format_timestamp(timestamp)}')

    # Memory logger.
    getattr(
        logging,
        _WarningLevels.logger_method(memory['warning_level'])
    )(f"Memory: {memory.get('val')} [MB]")

    # Time logger.
    getattr(
        logging,
        _WarningLevels.logger_method(time['warning_level'])
    )(f"Time: {time.get('val')} [s]\n")
