__all__ = []

import os


def _levels_options_valid(levels):
    """
    Validate levels options for legal possibilities.
    :param levels:
    :return:
    """
    valid = bool(levels)
    if levels:
        if levels.length != 2:
            valid = False
        elif levels[0] >= levels[1]:
            valid = False
        elif levels[0] <= 0 or levels[1] <= 0:
            valid = False

    return valid


def _log_path_valid(log_path):
    """
    If path is sent, make sure its a valid directory and
    we have write access to it.
    :param log_path: {String}
    :return: {Boolean}
    """
    if log_path:
        if not os.path.isdir(log_path):
            return False
        if not os.access(os.path.dirname(log_path), os.W_OK):
            return False
    return True


def _trailing_slash(path):
    """
    Make sure trailing slash exists in the path specified.
    :param path: {String}
    :return: {String}
    """
    if path and path[-1] != '/':
        return path + '/'
    return path


def _format_timestamp(time_object):
    """
    Format timestamp to string and add UTC timezone.
    :param time_object: {Datetime}
    :return: {String}
    """
    return '{} UTC'.format(time_object.strftime('%m-%d-%Y %H:%M:%S'))
