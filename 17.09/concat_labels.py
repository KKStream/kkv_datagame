"""
"""
import csv


root = '/Users/ironhead/datasets/datagames/1709/ans/'

header = [
    'userId',
    '624ans1', '624ans2', '624ans3', '624ans4',
    '625ans1', '625ans2', '625ans3', '625ans4',
    '626ans1', '626ans2', '626ans3', '626ans4',
    '627ans1', '627ans2', '627ans3', '627ans4',
    '628ans1', '628ans2', '628ans3', '628ans4',
    '629ans1', '629ans2', '629ans3', '629ans4',
    '630ans1', '630ans2', '630ans3', '630ans4'
]

lines = []

for i in range(60):
    path = root + 'ans-' + str(i).rjust(5, '0')

    print 'processing {}'.format(path)

    with open(path, 'rb') as csv_source_file:
        source_reader = csv.reader(csv_source_file, delimiter=',')

        next(source_reader)

        for line in source_reader:
            lines.append(line)

lines = sorted(lines, key=lambda x: x[0])

with open('./processed/labels_train.csv', 'wb') as csv_target_file:
    target_writer = csv.writer(csv_target_file, delimiter=',')

    target_writer.writerow(header)

    for line in lines:
        target_writer.writerow(line)
