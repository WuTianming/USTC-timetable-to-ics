import json, demjson
from icalendar import Calendar, Event
from datetime import datetime,timedelta
from pytz import UTC  # timezone
from pytz import timezone

cal = Calendar()
cal.add('prodid', '-//ustc timetable//timetable//CN')
cal.add('version', '2.0')
cal.add('TZID','Asia/Shanghai')
cal.add('X-WR-TIMEZONE','Asia/Shanghai')

MODE = "CN"
FIRST = datetime.strptime("2020-09-13 00:00:00","%Y-%m-%d %H:%M:%S").astimezone(timezone("Asia/Shanghai"))  # 学期第一周的周日，即开学前一天

s = str(open("1.json", 'r', encoding='UTF-8').readlines())
xx = demjson.decode(s)
x = (demjson.decode(xx[0]))
print(x['studentTableVm']['name'], x['studentTableVm']['code'], x['studentTableVm']['department'], "本学期学分",
      x['studentTableVm']['credits'], x['studentTableVm']['major'])
ii = 0
for c in x['studentTableVm']['activities']:
    summary = c['courseName']
    location = ' '.join([c['campus'] or c['customPlace'] or ' ', c['room'] or ' '])
    description = " ".join([c['campus'] or c['customPlace'] or ' ', c['building'] or ' ', " ".join(c['teachers']), c['weeksStr'] + "周", c['lessonCode'],
                            str(c['credits']) + '学分'])
    status = 0  # 0每周 1单周 2双周
    weeksStr = str(c['weeksStr'])
    if weeksStr.find("单") > -1:
        status = 1
        weeksStr=weeksStr.replace('单', '')
    elif weeksStr.find("双") > -1:
        status = 2
        weeksStr=weeksStr.replace('双', '')
    if status == 0:
        qaq = weeksStr.split(',');
        for it in qaq:
            if it.find('-') > -1:
                startWeek = int(it.split('-')[0])
                endWeek = int(it.split('-')[1])
            else:
                startWeek = int(it)
                endWeek = int(it)
            weekday = int(c['weekday'])
            if (weekday == 7):
                startWeek -= 1
                endWeek -= 1
            sHour=int(c['startDate'].split(':')[0])
            sMin = int(c['startDate'].split(':')[1])
            eHour=int(c['endDate'].split(':')[0])
            eMin = int(c['endDate'].split(':')[1])
            event = Event()
            event.add('summary', summary)
            event.add('location', location)
            event.add('description', description)
            event.add('dtstart',FIRST+timedelta(days=weekday,weeks=startWeek-1,hours=sHour,minutes=sMin))
            event.add('dtend', FIRST+timedelta(days=weekday,weeks=startWeek-1,hours=eHour,minutes=eMin))
            event.add('dtstamp', datetime.utcnow())
            interval = 2 if status else 1
            event.add('rrule', {'freq': 'weekly', 'interval': interval, 'count': (endWeek - startWeek) // interval + 1})
            cal.add_component(event)
    else:
        startWeek = int(weeksStr.split('-')[0])
        endWeek = int(weeksStr.split('-')[1])
        weekday = int(c['weekday'])
        if (weekday == 7):
            startWeek -= 1
            endWeek -= 1
        sHour=int(c['startDate'].split(':')[0])
        sMin = int(c['startDate'].split(':')[1])
        eHour=int(c['endDate'].split(':')[0])
        eMin = int(c['endDate'].split(':')[1])
        event = Event()
        event.add('summary', summary)
        event.add('location', location)
        event.add('description', description)
        event.add('dtstart',FIRST+timedelta(days=weekday,weeks=startWeek-1,hours=sHour,minutes=sMin))
        event.add('dtend', FIRST+timedelta(days=weekday,weeks=startWeek-1,hours=eHour,minutes=eMin))
        event.add('dtstamp', datetime.utcnow())
        interval = 2 if status else 1
        event.add('rrule', {'freq': 'weekly', 'interval': interval, 'count': (endWeek - startWeek) // interval + 1})
        cal.add_component(event)
f = open('output.ics', 'wb')
f.write(cal.to_ical())
f.close()
