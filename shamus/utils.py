def levels_options_valid(levels):
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


def trailing_slash(path):
    if path and path[-1] != '/':
        return path + '/'
    return path
    # TODO: check does this path actually exist, maybe do it all in validate?


def format_timestamp(time_object):
    return '{} UTC'.format(time_object.strftime('%m-%d-%Y %H:%M:%S'))
