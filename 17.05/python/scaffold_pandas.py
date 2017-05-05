"""
"""
import json
import pandas as pd


# all paths
path_events_train = './data/events_train.csv'
path_events_test = './data/events_test.csv'
path_labels_train = './data/labels_train.csv'
path_labels_test = './data/sample.csv'
path_titles_meta = './data/titles.json'
path_result = './data/python_pandas_results.csv'

# load csv
dtype_columns = {
    'time': object,
    'user_id': object,
    'title_id': object,
    'is_simulcast': object,
    'title_name': object,
    'watch_time': object,
}

events_train = pd.read_csv(path_events_train, dtype=dtype_columns)
events_test = pd.read_csv(path_events_test, dtype=dtype_columns)
labels_train = pd.read_csv(path_labels_train, dtype=dtype_columns)
labels_test = pd.read_csv(path_labels_test, dtype=dtype_columns)

with open(path_titles_meta) as f_titles:
    titles_meta = json.load(f_titles)


print(events_train.head())
print(events_test.head())
print(labels_train.head())
print(labels_test.head())
print('number of keys: {}'.format(len(titles_meta)))

# we want to guess title_id for user_id in events_test
# (they are 00000000 ~ 00041538 and in the sample.csv).
# change the title_id for each user_id to make a new result

labels_test['title_id'] = labels_test.apply(lambda row: '00000123', axis=1)

labels_test.to_csv(path_result, index=False)

print(labels_test.head())

# More Different Strategies
# * find the relationships between events_train and labels_train, use the
#   relationships to guess labels_test based on events_test
# * find the relationships between titles by examining titles
