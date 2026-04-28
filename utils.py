"""Модуль утилит."""


def get_formated_time(time: float) -> str:
    """Возвращает время в формате ЧЧ:ММ:СС."""
    time_total = round(time)
    hours = time_total // (60 * 60)
    minutes = (time_total // 60) % 60
    seconds = time_total % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"
