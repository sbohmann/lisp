from io import open
import re
from datetime import datetime, timedelta, time
from functools import reduce


def run():
    events = []
    for raw_line in open('input.txt'):
        line = raw_line.strip()
        events.append(Event(line))
    events.sort(key=lambda event: event.time)
    check_against_equal_times(events)
    days = Processor(events).run()
    sleepiest_guard = SleepyGuards(days).report()

    (maximum_minute, maximum, tainted) = PreferredMinute(sleepiest_guard, days).report()
    print(sleepiest_guard * maximum_minute, 'tainted:', tainted)

    (sleepiest_guard, maximum_minute, maximum) = PreferredGuardMinute(days).report()
    print(sleepiest_guard * maximum_minute)


def check_against_equal_times(events):
    last = None
    for event in events:
        if last is not None and event.time == last.time:
            raise ValueError('Found equal time at ' + str(event.time))
        last = event


_event_pattern = re.compile(
    '\[(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})\] (?:Guard #(\d+) begins shift|(falls asleep)|(wakes up))')


class Event:
    def __init__(self, description):
        match = _event_pattern.fullmatch(description)
        if match is None:
            raise ValueError('Illegal description: [' + description + ']')
        self.time = self.parse_time(match)
        self.call_handler = self._create_handler_call(match.groups()[5:8])

    def parse_time(self, match):
        return datetime(*map(int, match.groups()[0:5]))

    def _create_handler_call(self, event):
        self._check(event)
        if event[0] is not None:
            parsed_guard_id = int(event[0])
            return lambda handler: handler.guard(self.time, parsed_guard_id)
        elif event[1] is not None:
            return lambda handler: handler.asleep(self.time)
        elif event[2] is not None:
            return lambda handler: handler.awake(self.time)

    def _check(self, event):
        defined_events = reduce(lambda n, group: n if group is None else n + 1, event, 0)
        if defined_events != 1:
            raise AssertionError()


class GuardSwitch:
    def __init__(self, time, id):
        self.time = time
        self.id = id

    def __str__(self) -> str:
        return 'GuardSwitch(time: ' + str(self.time) + ', id: ' + str(self.id) + ')'


class Processor:
    def __init__(self, events):
        self.events = events
        self._last_guard_switch = None
        self._days = []
        self._current_day = None

    def run(self):
        for event in self.events:
            self._fill_minutes(event.time)
            self._handle_day_change(event.time)
            event.call_handler(self)
        self._finish()
        return self._days

    def _fill_minutes(self, time):
        if self._current_day != None:
            self._current_day.fill_minutes(time)

    def _handle_day_change(self, time):
        recording_date = (time + timedelta(hours=2)).date()
        if self._current_day == None or self._current_day.date != recording_date:
            if self._current_day is not None:
                self._current_day.finish()
            self._current_day = DayRecording(recording_date, self._current_guard_or_none(time))
            self._days.append(self._current_day)

    def guard(self, time, id):
        self._last_guard_switch = GuardSwitch(time, id)
        self._current_day.guard(time, id)

    def asleep(self, time):
        self._current_day.asleep(time)

    def awake(self, time):
        self._current_day.awake(time)

    def _current_guard(self, time):
        result = self._current_guard_or_none(time)
        if result is not None:
            return result
        else:
            raise ValueError(
                'No last guard found @ ' + str(time) + ' - last guard switch @ ' + str(self._last_guard_switch))

    def _current_guard_or_none(self, time):
        if self._last_guard_switch is not None and self._sufficiently_recent(self._last_guard_switch.time, time):
            return self._last_guard_switch.id
        else:
            return None

    def _sufficiently_recent(self, time, now):
        delta = now - time
        return delta >= timedelta() and delta <= timedelta(hours=2)

    def _finish(self):
        if self._current_day is not None:
            self._current_day.finish()


class Record:
    def __init__(self, guard, asleep):
        self.guard = guard
        self.asleep = asleep


class DayRecording:
    def __init__(self, date, guard_id):
        self.data: [Record] = [None] * 60
        self.date = date
        self._guard_id = guard_id
        self._asleep = False
        self._next_minute = 0

    def guard(self, time, id):
        self.fill_minutes(time)
        self._guard_id = id
        self._asleep = False

    def asleep(self, time):
        self.fill_minutes(time)
        self._asleep = True

    def awake(self, time):
        self.fill_minutes(time)
        self._asleep = False

    def finish(self):
        self._fill_minutes_to_end(self._hour_end_as_datetime())
        if len(self.data) != 60:
            raise AssertionError()

    def fill_minutes(self, time):
        end = self._hour_end_as_datetime()
        if time < end:
            end = time
        self._fill_minutes_to_end(end)

    def _fill_minutes_to_end(self, end):
        minute = self._next_minute_as_datetime()
        step = timedelta(minutes=1)
        while minute < end:
            self.data[minute.minute] = Record(self._guard_id, self._asleep)
            minute += step
        self._next_minute = 60 * minute.hour + minute.minute

    def _next_minute_as_datetime(self):
        return datetime.combine(self.date, time(hour=self._next_minute // 60, minute=self._next_minute % 60))

    def _hour_end_as_datetime(self):
        return datetime.combine(self.date, time(hour=1))


class SleepyGuards:
    def __init__(self, days):
        self._days = days
        self._sleeping_minutes_for_guard = {}
        self._calculate()

    def _calculate(self):
        for day in self._days:
            for record in day.data:
                self._register_record(record)

    def _register_record(self, record):
        if record.guard is not None:
            value = self._sleeping_minutes_for_guard.get(record.guard, 0)
            if record.asleep:
                value += record.asleep
            self._sleeping_minutes_for_guard[record.guard] = value

    def report(self):
        data = list(self._sleeping_minutes_for_guard.items())
        data.sort(key=lambda entry: entry[1], reverse=True)
        sleepiest_guard = data[0][0]
        print('sleepiest guard:', sleepiest_guard)
        return sleepiest_guard


class PreferredMinute(object):
    def __init__(self, guard, days):
        self._guard = guard
        self._days = days
        self._minutes = [0] * 60
        self._calculate()

    def _calculate(self):
        for day in self._days:
            for minute in range(0, 60):
                record = day.data[minute]
                self._register_record(record, minute)

    def _register_record(self, record, minute):
        if record.guard == self._guard and record.asleep:
            self._minutes[minute] = self._minutes[minute] + 1

    def report(self):
        maximum = -1
        maximum_minute = None
        tainted = True
        for minute in range(0, 60):
            value = self._minutes[minute]
            if value > maximum:
                maximum = value
                maximum_minute = minute
                tainted = False
            elif value == maximum:
                tainted = True
        return (maximum_minute, maximum, tainted)


class PreferredGuardMinute:
    def __init__(self, days):
        self._days = days
        self._collect_guards()
        self._calculate()

    def _collect_guards(self):
        self._guards = set()
        for day in self._days:
            for record in day.data:
                self._guards.add(record.guard)

    def _calculate(self):
        self._entries = []
        for guard in self._guards:
            (maximum_minute, maximum, tainted) = PreferredMinute(guard, self._days).report()
            print(guard, maximum_minute, maximum, tainted)
            self._entries.append((guard, maximum_minute, maximum))
        self._entries.sort(key=lambda entry: entry[2], reverse=True)

    def report(self):
        return self._entries[0]


run()
