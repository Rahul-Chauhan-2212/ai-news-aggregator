from datetime import datetime, timedelta


def parse_rss_date(entry, field_name):
    struct = getattr(entry, f"{field_name}_parsed", None)
    if not struct:
        return None
    return datetime(*struct[:6])


def last_n_days_cutoff(days=6):
    return datetime.now() - timedelta(days=days)


def within_last_n_days(dt, days=6):
    if not dt:
        return False
    return dt >= last_n_days_cutoff(days)
