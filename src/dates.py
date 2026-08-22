from datetime import datetime
from typing import Optional

DATE_FORMATS = [
    "%Y-%m-%d",
    "%d/%m/%Y",
    "%m.%d.%Y",
    "%b %d, %Y",
    "%Y/%m/%d",
]


def get_date(date_input: Optional[str]) -> str:
    """
    Нормализует дату в YYYY-MM-DD.
    Если None/пусто → "". Иначе пытается распарсить по DATE_FORMATS.
    Если не удалось → ValueError.
    """
    if date_input is None or date_input == "":
        return ""

    date_str = str(date_input).strip()
    if not date_str:
        return ""

    for fmt in DATE_FORMATS:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue

    raise ValueError(f"Unable to parse date: {date_input!r}")


from datetime import datetime
from typing import Optional

DATE_FORMATS = [
    "%Y-%m-%d",
    "%d/%m/%Y",
    "%m.%d.%Y",
    "%b %d, %Y",
    "%Y/%m/%d",
]


def get_date(date_input: Optional[str]) -> str:
    if date_input is None or date_input == "":
        return ""

    date_str = str(date_input).strip()
    if not date_str:
        return ""

    for fmt in DATE_FORMATS:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue

    raise ValueError(f"Unable to parse date: {date_input!r}")


from datetime import datetime
from typing import Optional

DATE_FORMATS = [
    "%Y-%m-%d",
    "%d/%m/%Y",
    "%m.%d.%Y",
    "%b %d, %Y",
    "%Y/%m/%d",
]


def get_date(date_input: Optional[str]) -> str:
    if date_input is None or date_input == "":
        return ""

    date_str = str(date_input).strip()
    if not date_str:
        return ""

    for fmt in DATE_FORMATS:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue

    raise ValueError(f"Unable to parse date: {date_input!r}")