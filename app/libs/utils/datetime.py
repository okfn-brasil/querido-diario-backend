from django.utils import timezone

date_format_default = "%d/%m/%Y"
date_format_diario = "%Y-%m-%d"

datetime_format_diario = "%Y-%m-%dT%H:%M:%S"


def datetime_to_date_str(date: timezone.datetime) -> str:
    return date.strftime(date_format_default)


def datetime_to_date_str_diario(date: timezone.datetime) -> str:
    return date.strftime(date_format_diario)


def datetime_to_datetime_str_diario(date: timezone.datetime) -> str:
    return date.strftime(datetime_format_diario)


def datetime_from_date_str(date: str) -> timezone.datetime:
    return timezone.datetime.strptime(
        date,
        date_format_default,
    )


def datetime_from_date_str_diario(date: str) -> timezone.datetime:
    return timezone.datetime.strptime(
        date,
        date_format_diario,
    )
