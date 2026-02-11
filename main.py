import logging

from sqlalchemy.orm import Session

from database import DB_ENGINE, Record
from logger import get_sql_logger


def main() -> None:
    sql_logger = get_sql_logger("custom_logger", logging.INFO)

    sql_logger.debug("This will not be sent to SQL.")
    sql_logger.info("This will be sent to SQL.")
    sql_logger.critical("Big mistake, huge!")

    # Print all logs
    session = Session(bind=DB_ENGINE)
    records = session.query(Record).all()

    for record in records:
        print(f"{record.timestamp}: ({record.log_level}) {record.log_message}")  # noqa: T201


if __name__ == "__main__":
    main()
