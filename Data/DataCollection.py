from everywhereml.data import Dataset

dataset = Dataset.from_csv('data.csv', name='ContinuousMotion', target_column='label')
dataset.describe()