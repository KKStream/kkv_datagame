"""
* consider last 25 weeks
* ~0.7303
"""
import csv


table = [28800.0, 28800.0, 14400.0, 14400.0]


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

            total_weight = 0.0

            for line in source_reader:
                userid = [line[0]]
                labels = [0.0] * 28

                for i in xrange(25, 697, 28):
                    weight = 1.0 + (i - 25) / 28.0

                    total_weight += weight

                    for j in xrange(28):
                        prob = min(1.0, int(line[i + j]) / 2400.0)

                        labels[j] += weight * prob

                        # labels[j] += weight * int(line[i + j]) / table[j % 4]

                labels = [x / total_weight for x in labels]

                target_writer.writerow(userid + labels)


test()
