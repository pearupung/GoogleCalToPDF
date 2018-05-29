from datetime import datetime, timedelta

from reportlab.lib import pagesizes
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Frame, Spacer, KeepInFrame
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

from DataCollector import Collector
from DataCollector.Collector import datetime_from_rfc3339
from DataCollector.googleCalAPI import api_setup

frame_width = 2 * cm
frame_height = 5.5 * cm

def get_event_paragraph(event, spaceAfter=0, borderPadding=2):

    event_style = ParagraphStyle(
        "event",
        fontName="Times-Roman",
        fontSize=5,
        backColor=event['color'],
        textColor='white',
        leading=6,
        borderPadding=borderPadding,
        spaceAfter=spaceAfter + 2 * borderPadding
    )

    beginTime = event['start'].strftime("%H:%M")
    endTime = event['end'].strftime("%H:%M")

    eventStringList = [f"<b>{beginTime}-{endTime}</b>"]

    eventStringList.append(event['summary'])

    return Paragraph(' '.join(eventStringList), event_style)


def fill_frames(service, frame1, frame2, date, canv):


    events = Collector.collect_date_events(service, date)

    half = len(events) // 2
    add_events_to_frame(frame1, events[:half], canv)
    add_events_to_frame(frame2, events[half:], canv)

    return frame1, frame2

def add_events_to_frame(frame, events, canvas):

    story = []
    free_space = frame.height

    for event in events:
        paragraph = get_event_paragraph(event)
        story.append(paragraph)
        free_space -= paragraph.wrap(frame_width, frame_height)[1] - 1

    real_story = []

    if free_space > 0:
        spaces = Collector.get_space_after(events, free_space)
    for i, paragraph in enumerate(story):
        real_story.append(paragraph)
        real_story.append(Spacer(1, spaces[i] + 1))
    frame.addFromList(real_story, canvas)
    return frame


def draw_day_first_format(service, canvas, date, i=0, j=0):
    frame1 = Frame(i * 7 * cm, pagesizes.A4[1] - (j + 1) * frame_height,
                   frame_width, frame_height, showBoundary=1,
                   topPadding=6, bottomPadding=6)
    frame2 = Frame((i* 7 + 3.5) * cm, pagesizes.A4[1] - (j + 1) * frame_height,
                   frame_width, frame_height, showBoundary=1,
                   topPadding=6, bottomPadding=6)
    fill_frames(service, frame1, frame2, date, canvas)

    pass

def main():
    c = canvas.Canvas("../example.pdf", pagesize=pagesizes.A4)
    serv = api_setup()
    story = []
    for j in range(0, 4):
        for i in range(0, 2):

            print(j*2+i)
            date = datetime(2018, 5, 29) + timedelta(days=j*2+i)
            draw_day_first_format(serv, c, date, i, j)


    c.showPage()
    c.save()

if __name__ == "__main__":
    main()