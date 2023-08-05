from datetime import datetime


def _plurality(x: int) -> str:
    return "" if x == 1 else "s"


def get_time_difference(input_datetime: datetime) -> str:
    now = datetime.now()

    if (x := now.year - input_datetime.year) != 0:
        return f"{x} year{_plurality(x)} ago"

    if (x := now.month - input_datetime.month) != 0:
        return f"{x} month{_plurality(x)} ago"

    if (x := now.day - input_datetime.day) != 0:
        return f"{x} day{_plurality(x)} ago"

    if (x := now.hour - input_datetime.hour) != 0:
        return f"{x} hour{_plurality(x)} ago"

    if (x := now.minute - input_datetime.minute) != 0:
        return f"{x} minute{_plurality(x)} ago"

    if (x := now.second - input_datetime.second) != 0:
        return f"{x} second{_plurality(x)} ago"

    raise Exception("unexpected error")
