from term_colors import TermColors


class WarningLevels:
    OK = 'ok'
    WARNING = 'warning'
    CRITICAL = 'critical'

    @staticmethod
    def term_color(level):
        return {
            WarningLevels.OK: TermColors.OK_GREEN,
            WarningLevels.WARNING: TermColors.WARNING,
            WarningLevels.CRITICAL: TermColors.FAIL
        }[level]

    @staticmethod
    def logger_method(level):
        return {
            WarningLevels.OK: 'info',
            WarningLevels.WARNING: 'warning',
            WarningLevels.CRITICAL: 'critical'
        }[level]
