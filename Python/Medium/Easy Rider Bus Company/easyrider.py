import json
from collections import defaultdict
import re
from datetime import datetime, time

FIELDS = ["bus_id", "stop_id", "stop_name", "next_stop", "stop_type", "a_time"]
FORMAT_FIELDS = ["stop_name", "stop_type", "a_time"]

BUS_ID = 'bus_id'
STOP_ID = 'stop_id'
STOP_NAME = 'stop_name'
NEXT_STOP = 'next_stop'
STOP_TYPE = 'stop_type'
A_TIME = 'a_time'


def main():
    data = json.loads(input())
    find_type_and_required_errors(data)
    find_format_errors(data)
    find_number_of_stops(data)
    find_stops_types(data)
    validate_arrival_time(data)
    get_bad_stops(data)


# Stage 1
def find_type_and_required_errors(data):
    errors = defaultdict(lambda: 0)
    for record in data:
        for int_field in (BUS_ID, STOP_ID, NEXT_STOP):
            if type(record[int_field]) != int:
                errors[int_field] += 1
        for str_field in (STOP_NAME, A_TIME):
            if not (type(record[str_field]) == str and len(record[str_field]) > 0):
                errors[str_field] += 1
        if not (type(record[STOP_TYPE]) == str and len(record[STOP_TYPE]) <= 1):
            errors[STOP_TYPE] += 1

    print(f"Type and required field validation: {sum(errors.values())} errors")
    for field in FIELDS:
        print(f"{field}: {errors[field]}")


# Stage 2
def find_format_errors(data):
    errors = defaultdict(lambda: 0)
    for record in data:
        if not re.match(r'^[A-Z].+(Road|Avenue|Boulevard|Street)$', record[STOP_NAME]):
            errors[STOP_NAME] += 1
        if record[STOP_TYPE] not in ('', 'S', 'O', 'F'):
            errors[STOP_TYPE] += 1
        if not re.match(r'^[0-2]\d:[0-5]\d$', record[A_TIME]):
            errors[A_TIME] += 1

    print(f"Format validation: {sum(errors.values())} errors")
    for field in FORMAT_FIELDS:
        print(f"{field}: {errors[field]}")


# Stage 3
def find_number_of_stops(data):
    bus_stops = defaultdict(lambda: 0)
    for record in data:
        bus_stops[record['bus_id']] += 1

    print("Line names and number of stops:")
    for bus, stops in bus_stops.items():
        print(f"bus_id: {bus}, stops: {stops}")


# Stage 4
def find_stops_types(data):
    start_stops = set()
    possible_transfer_stops = set()
    transfer_stops = set()
    finish_stops = set()
    starts = {}
    finishes = {}
    busses = set()
    for record in data:
        busses.add(record[BUS_ID])
        if record[STOP_TYPE] == 'S':
            start_stops.add(record[STOP_NAME])
            starts[record[BUS_ID]] = True
        elif record[STOP_TYPE] == 'F':
            finish_stops.add(record[STOP_NAME])
            finishes[record[BUS_ID]] = True
        if record[STOP_NAME] in possible_transfer_stops:
            transfer_stops.add(record[STOP_NAME])
        else:
            possible_transfer_stops.add(record[STOP_NAME])

    try:
        for bus in busses:
            if not (bus in starts and bus in finishes):
                print("There is no start or end stop for the line:", bus)
                raise ValueError
    except ValueError:
        pass
    else:
        print('Start stops:', len(start_stops), sorted(start_stops))
        print('Transfer stops:', len(transfer_stops), sorted(transfer_stops))
        print('Finish stops:', len(finish_stops), sorted(finish_stops))


# Stage 5
def validate_arrival_time(data):
    print('Arrival time test:')
    busses = get_busses(data)
    good = True

    for bus in busses:
        bus_data = [record for record in data if record[BUS_ID] == bus]
        last_time = time()
        for record in bus_data:
            curr_time = datetime.strptime(record[A_TIME], '%H:%M').time()
            if curr_time <= last_time:
                good = False
                print(f'bus_id line {record[BUS_ID]}: wrong time on station {record[STOP_NAME]}')
                break
            last_time = curr_time

    if good:
        print('OK')


def get_busses(data):
    busses = set()
    for record in data:
        busses.add(record[BUS_ID])
    return busses


# Stage 6
def get_bad_stops(data):
    print('On demand stops test:')
    transfer_stops = find_transfer_stops(data)
    bad_stops = set()

    for record in data:
        if record[STOP_TYPE] == 'O' and record[STOP_NAME] in transfer_stops:
            bad_stops.add(record[STOP_NAME])

    if bad_stops:
        print('Wrong stop type:', sorted(bad_stops))
    else:
        print('OK')


def find_transfer_stops(data):
    possible_transfer_stops = set()
    transfer_stops = set()
    for record in data:
        if record[STOP_NAME] in possible_transfer_stops:
            transfer_stops.add(record[STOP_NAME])
        else:
            possible_transfer_stops.add(record[STOP_NAME])

    return transfer_stops


if __name__ == '__main__':
    main()
