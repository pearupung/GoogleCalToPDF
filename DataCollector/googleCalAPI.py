from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from reportlab.lib import pagesizes
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime, timezone, timedelta

# Setup the Calendar API
def api_setup():
    SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
    store = file.Storage(r'/home/pearu/PycharmProjects/untitled/credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    return service

def get_events(service, calendar, date):
    end = date + timedelta(days=1)

    events_result = service.events().list(
        calendarId=calendar,
        orderBy="startTime",
        singleEvents=True,
        timeMin=date.isoformat() + 'Z',
        timeMax=end.isoformat() + 'Z').execute()

    events = events_result.get("items", [])
    return events


def get_colors(service):
    colors = service.colors().get().execute()
    return colors


def get_calendars(service):
    """
    Get all calendar id-s.
    :param service:
    :return:
    """
    calendars = service.calendarList().list().execute().get('items', [])
    return calendars
