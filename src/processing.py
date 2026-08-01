from datetime import datetime
from typing import Any, Dict, List


def filter_by_state(records: List[Dict[str, Any]], state: str) -> List[Dict[str, Any]]:
    """
    Фильтрует записи по точному совпадению record.get("state") == state.
    Пустой список → []. Записи без "state" игнорируются.
    """
    if not records:
        return []
    return [r for r in records if r.get("state") == state]


def sort_by_date(records: List[Dict[str, Any]], reverse: bool = False, date_key: str = "date") -> List[Dict[str, Any]]:
    """
    Сортирует записи по дате (key=date_key) в формате YYYY-MM-DD.
    reverse=False → возрастание, reverse=True → убывание.
    Записи без валидной даты помещаются в конец списка.
    """

    def safe_date(record: Dict[str, Any]) -> datetime | None:
        date_val = record.get(date_key)
        if not isinstance(date_val, str):
            return None
        try:
            return datetime.strptime(date_val, "%Y-%m-%d")
        except ValueError:
            return None

    def sort_key(record: Dict[str, Any]):
        d = safe_date(record)
        # Валидные даты раньше, None — в конце
        return (d is None, d)

    return sorted(records, key=sort_key, reverse=reverse)


from typing import Any, Dict, List


def filter_by_state(records: List[Dict[str, Any]], state: str) -> List[Dict[str, Any]]:
    if not records:
        return []
    return [r for r in records if r.get("state") == state]
