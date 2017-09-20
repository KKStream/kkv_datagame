"""
if I watched tv last Monday night, I probably will watch tv this Monday night.
"""
import auc
import csv


def validate():
    """
    """
    labels_guess = []
    labels_truth = []

    path_source = './processed/consumption_train.csv'
    path_target = './processed/labels_train.csv'

    with open(path_source, 'rb') as csv_source_file:
        source_reader = csv.reader(csv_source_file, delimiter=',')

        for line in source_reader:
            labels = [0 if x == '0' else 1 for x in line[-56:-28]]

            labels_guess.extend(labels)

    with open(path_target, 'rb') as csv_target_file:
        target_reader = csv.reader(csv_target_file, delimiter=',')

        next(target_reader)

        for line in target_reader:
            labels_truth.extend([int(x) for x in line[1:]])

    print auc.auc(labels_guess, labels_truth)


def test():
    """
    """
    path_source = './processed/consumption_test.csv'
    path_target = './result.csv'

    with open(path_target, 'wb') as csv_target_file:
        target_writer = csv.writer(csv_target_file, delimiter=',')

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

        target_writer.writerow(header)

        with open(path_source, 'rb') as csv_source_file:
            source_reader = csv.reader(csv_source_file, delimiter=',')

            for line in source_reader:
                userid = [line[0]]
                labels = [0 if x == '0' else 1 for x in line[-56:-28]]

                target_writer.writerow(userid + labels)


validate()
# test()
