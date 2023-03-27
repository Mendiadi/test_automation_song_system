import logging
from typing import Literal, Any
import sys


class Logger:
    """Basic Wrapper for logger"""
    D_LOG_FILE = 'logs.txt'
    D_LOG_FMT = '%(asctime)-4s [%(levelname)-4s] %(message)s'
    D_TIME_FMT = '%Y-%m-%d %H:%M:%S'

    def __init__(self, name: str, format=D_LOG_FMT, datefmt=D_TIME_FMT, file=D_LOG_FILE):
        """Setting up the logger, config the format printing,
           set datetime format, set file, levels, handler
           :param name: string
           :return Logger type object"""
        self._logger = logging.getLogger(name)
        self._formatter = None
        self._file_handler = None
        self._screen_handler = None
        self.set_formatter(format, datefmt)
        self.setup_file(file)
        self.setup_cli(sys.stdout)
        self.set_lvl(logging.INFO)
        self._LOG_LEVELS = dict(
            info=self._logger.info,
            error=self._logger.error,
            warning=self._logger.warning
        )

    @property
    def logger(self):
        """get logger"""
        return self._logger

    def set_formatter(self, fmt=D_TIME_FMT, datefmt=D_TIME_FMT, **options):
        """Setting or replacing the log format"""
        self._formatter = logging.Formatter(fmt, datefmt, **options)
        for h in self.logger.handlers:
            h.setFormatter(self._formatter)

    def set_lvl(self, lvl: int):
        """setting the log level"""
        self._logger.setLevel(lvl)

    def _swap_handlers(self, handle, handle_type, **args):
        """Take handler and replace with old one"""
        self._logger.removeHandler(handle)
        handle = handle_type(**args)
        handle.setFormatter(self._formatter)
        self._logger.addHandler(handle)

    def setup_file(self, filename: str):
        """Set file as log output"""
        self._swap_handlers(self._file_handler,
                            logging.FileHandler,
                            filename=filename,
                            mode="w")

    def setup_cli(self, stream: Any):
        """Set log to cli stream"""
        self._swap_handlers(self._screen_handler,
                            logging.StreamHandler,
                            stream=stream)

    def log(self,
            *messages: str,
            level: Literal["info", "warning", "error"] = "info",
            attach_origin: str = None
            ):
        """
        Main log functions
        :param messages: strings formats to log
        :param level: info , error , warning
        :param attach_origin: log name of func and file if True
        """
        args_len = len(messages)
        messages = [msg for msg in messages if type(msg) is str]
        if args_len != len(messages):
            self._logger.warning("(log error) you try to pass a not string arguments... just removed.")
        log_handler = self._LOG_LEVELS.get(level)
        if not log_handler:
            self._logger.warning(f"(log error) level argument ({level}) not supported... info choose instead.")
            log_handler = self._LOG_LEVELS["info"]
        origin = f"{attach_origin} > " if attach_origin else ""
        log_handler(origin + " ".join(messages))


# globals loggers
logger = Logger("mylogger")
unit_logger = Logger("unit test")
