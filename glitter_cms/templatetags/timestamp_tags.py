import datetime
from django import template
register = template.Library()


def display_timestamp(timestamp):
    try:
        float_timestamp = float(timestamp)
    except ValueError:
        return ""
    return datetime.datetime.fromtimestamp(float_timestamp)


register.filter(display_timestamp)