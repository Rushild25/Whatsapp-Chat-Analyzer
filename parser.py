import re
import pandas as pd

def parse_whatsapp_chat(file):
    raw = file.read()

    data = None
    for encoding in ('utf-8-sig', 'utf-8', 'utf-16', 'latin-1'):
        try:
            data = raw.decode(encoding)
            break
        except UnicodeDecodeError:
            continue

    if data is None:
        data = raw.decode('utf-8', errors='replace')

    data = data.replace('\u202f', ' ').replace('\xa0', ' ')

    line_pattern = re.compile(
        r'^\[?(?P<date>\d{1,2}[/-]\d{1,2}[/-]\d{2,4}),\s'
        r'(?P<time>\d{1,2}:\d{2}(?::\d{2})?(?:\s?[APMapm]{2})?)\]?\s(?:-\s)?'
        r'(?P<text>.*)$'
    )

    records = []
    current_date = None
    current_time = None
    current_text = []

    for line in data.splitlines():
        match = line_pattern.match(line.strip())

        if match:
            if current_date is not None:
                records.append([current_date, current_time, '\n'.join(current_text).strip()])

            current_date = match.group('date').replace('-', '/')
            current_time = match.group('time').strip()
            current_text = [match.group('text').strip()]
        elif current_date is not None:
            current_text.append(line)

    if current_date is not None:
        records.append([current_date, current_time, '\n'.join(current_text).strip()])

    parsed_records = []
    for date, time, text in records:
        user = 'group_notification'
        message = text

        if ': ' in text:
            potential_user, msg = text.split(': ', 1)
            if len(potential_user) <= 34 and not potential_user.endswith('.'):
                user = potential_user
                message = msg

        parsed_records.append([date, time, user, message])

    return pd.DataFrame(parsed_records, columns=['date', 'time', 'user', 'message'])