import datetime as dt
from logging import Handler, Logger, LogRecord, getLevelName, getLogger

from sqlalchemy.orm import Session

from database import DB_ENGINE, Record


class SQLHandler(Handler):
    def __init__(self, level: int | str = 0) -> None:
        self._sesh = Session(DB_ENGINE)
        super().__init__(level)

    def emit(self, record: LogRecord) -> None:
        """
        Custom emit function to send log record to SQL database.

        Assumes the target SQL table has the following schema:
            file_name: name of .py file that triggered the log record.
            function_name: function that emitted the log record.
            log_level: one of DEBUG, INFO, WARNING, ERROR, CRITICAL.
            message: log message.
            timestamp: timestamp of log message
        """
        new_record = Record(
            file_name=record.filename,
            function_name=record.funcName,
            log_level=getLevelName(record.levelno),
            log_message=record.getMessage(),
            timestamp=dt.datetime.now(),
        )

        self._sesh.add(new_record)
        self._sesh.commit()


def get_sql_logger(logger_name: str, log_level: str | int) -> Logger:
    logger = getLogger(logger_name)
    logger.setLevel(log_level)
    handler = SQLHandler(log_level)
    logger.addHandler(handler)

    return logger
