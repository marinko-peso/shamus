__all__ = []

from .term_colors import _TermColors


class _WarningLevels:
    OK = 'ok'
    WARNING = 'warning'
    CRITICAL = 'critical'

    @staticmethod
    def term_color(level):
        return {
            _WarningLevels.OK: _TermColors.OK_GREEN,
            _WarningLevels.WARNING: _TermColors.WARNING,
            _WarningLevels.CRITICAL: _TermColors.FAIL
        }[level]

    @staticmethod
    def logger_method(level):
        """
        Choosing python logging method based on warning level.
        :param level: {String}
        :return:
        """
        return {
            _WarningLevels.OK: 'info',
            _WarningLevels.WARNING: 'warning',
            _WarningLevels.CRITICAL: 'critical'
        }[level]
