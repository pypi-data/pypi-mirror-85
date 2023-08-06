from datetime import datetime

import dateutil.parser
import pytz


def now_utc() -> datetime:
    return datetime.utcnow().replace(tzinfo=pytz.utc)


def parse_date(date_str: str) -> datetime:
    return dateutil.parser.parse(date_str)
