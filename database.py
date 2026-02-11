from enum import StrEnum

from sqlalchemy import Column, DateTime, Enum, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

DB_ENGINE = create_engine("sqlite:///example.db")


class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


Base = declarative_base()


class Record(Base):
    __tablename__ = "python_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_name = Column(String(50), nullable=False)
    function_name = Column(String(100), nullable=False)
    log_level = Column(Enum(LogLevel), nullable=False)
    log_message = Column(String(1000), nullable=False)
    timestamp = Column(DateTime, nullable=False)


Base.metadata.create_all(DB_ENGINE)
