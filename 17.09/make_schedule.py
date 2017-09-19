"""
"""
import csv

from six.moves import range


def timestamp_to_index(ts):
    """
    expected format: 2017-01-02 06:27:49

    2017-01-01: [0], [1], [2], [3]
    2017-01-02: [4], [5], [6], [7]
    ...
    2017-06-30: [720], [721], [722], [723]
    """
    segments = ts.replace(' ', '-').replace(':', '-').split('-')

    segments = [int(s) for s in segments]

    # based on segments[1] which is month
    index = [0, 31, 59, 90, 120, 151, 181][segments[1] - 1]

    # count date of month
    index += (segments[2] - 1)

    # 4 segments for each day
    index *= 4

    # begin at yesterday
    index -= 1

    # count the hour
    h, m, s = segments[3:]

    if h < 1:
        offset = 0
    elif h < 9:
        offset = 1
    elif h < 17:
        offset = 2
    elif h < 21:
        offset = 3
    else:
        offset = 4

    index += offset
    past = ((h + [3, -1, -9, -17, -21][offset]) * 60 + m) * 60 + m

    return index, past


def timestamp_duration_to_consumptions(timestamp, duration_s):
    """
    split session accross several segments.

    return:
        [(i, s0), (i+1, s1), ..., (i+n, sn)]
    """
    index, past = timestamp_to_index(timestamp)

    consumptions = []

    duration_s_table = [28800, 28800, 14400, 14400]

    while duration_s > 0:
        segment_duration = duration_s_table[index % 4]

        consumption = (index, min(segment_duration - past, duration_s))

        consumptions.append(consumption)

        duration_s -= (segment_duration - past)
        index += 1
        past = 0

    return consumptions


def aggregate_log(log_paths):
    """
    build schedule from a log file.
    a dictionary:
        key: user_id
        value: segmented consumption (724 segments)

    {
        123: [s0, s1, s2, ..., s723]
    }
    """
    schedule = {}

    for log_path in log_paths:
        print 'processing: {}'.format(log_path)

        with open(log_path, 'rb') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')

            next(reader)

            for line in reader:
                user_id = int(line[3])
                timestamp = line[7]
                duration_s = int(line[8])

                consumptions = \
                    timestamp_duration_to_consumptions(timestamp, duration_s)

                if user_id not in schedule:
                    schedule[user_id] = [0] * 724

                for cons in consumptions:
                    schedule[user_id][cons[0]] += cons[1]

    return schedule


def write_schedule(path, schedule):
    """
    write schedule (a dictionary) to a csv file.
    """
    keys = sorted(schedule.keys())

    with open(path, 'wb') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')

        for key in keys:
            line = [key] + schedule[key]

            csv_writer.writerow(line)


if __name__ == '__main__':
    root = '/Users/ironhead/datasets/datagames/1709/log/'

    log_paths_train = []
    log_paths_test = []

    # NOTE: training set: log-00000 ~ log-00059
    for i in range(60):
        path = root + 'log-000' + str(i).rjust(2, '0')

        log_paths_train.append(path)

    # NOTE: test set: log-00060 ~ log-00099
    for i in range(60, 100):
        path = root + 'log-000' + str(i).rjust(2, '0')

        log_paths_test.append(path)

    schedule_train = aggregate_log(log_paths_train)
    schedule_test = aggregate_log(log_paths_test)

    write_schedule('./processed/consumption_train.csv', schedule_train)
    write_schedule('./processed/consumption_test.csv', schedule_test)
