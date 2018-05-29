from datetime import datetime, timedelta, timezone
from DataCollector import googleCalAPI
import decimal

def datetime_from_rfc3339(timestring):
    date, time = timestring.split('T')
    returnValue = datetime(
        year=int(date[:4]),
        month=int(date[5:7]),
        day=int(date[8:10]),
        hour=int(time[:2]),
        minute=int(time[3:5]),
        second=int(time[6:8]),
        tzinfo=timezone(timedelta(hours=int(time[9:11])))
    )
    return returnValue


def zero_hour(date):
    return datetime(
        year=date.year,
        month=date.month,
        day=date.day,
        hour=0,
        minute=0,
        second=0,
        tzinfo=timezone(timedelta(hours=3))
    )



def convert_rgb(hex_str):
    h = hex_str.lstrip('#')
    rt = tuple((1/256) * int(h[i:i+2], 16) for i in (0, 2 ,4))
    return rt


def collect_date_events(service, date):
    """
    Collect all events from different calendars, get colours and durations and spaceAfters.
    :param service:
    :param date:
    :return:
    """
    colors = googleCalAPI.get_colors(service)
    events = []

    for calendar in googleCalAPI.get_calendars(service):
        calendar_events = googleCalAPI.get_events(service, calendar['id'], date)
        for calendar_event in calendar_events:
            event = {}
            event_keys = calendar_event.keys()
            event['summary'] = calendar_event['summary']
            event['start'] = datetime_from_rfc3339(calendar_event['start']['dateTime']) \
                if 'dateTime' in calendar_event['start'] \
                    else zero_hour(date)
            event['end'] = datetime_from_rfc3339(calendar_event['end']['dateTime']) \
                if 'dateTime' in calendar_event['end'] \
                    else zero_hour(date)

            event['location'] = calendar_event['location'] if 'location' in event_keys else None
            event['color'] = colors['event'][calendar_event['colorId']]['background'] \
                if 'colorId' in calendar_event.keys() \
                else colors['calendar'][calendar['colorId']]['background']
            events.append(event)
    return sorted(events, key=lambda x: x['start'])


#def collect_weeks_events(service, begindate, )


def get_space_after(events, free_space):
    """
    Calculate spaces between events in percentages based on sum of free time and constraints.

    :param events:
    :return:
    """
    timesum = timedelta(seconds=1)
    time_list = []

    for i in range(len(events) - 1):
        time_diff = events[i + 1]['start'] - events[i]['end']
        timesum += time_diff
        time_list.append(time_diff)

    time_list.append(timedelta(hours=0))

    spaces = []

    for diff in time_list:
        spaces.append(round(diff/timesum * free_space, 4))
    return spaces
