from everywhereml.preprocessing import Pipeline, MinMaxScaler, Window, SpectralFeatures
from everywhereml.data import Dataset

dataset = Dataset.from_csv('data.csv', name='ContinuousMotion', target_column='label')
dataset.describe()

sampling_frequency = 104
mean_gesture_duration_in_millis = 1000
window_length_seconds = sampling_frequency * mean_gesture_duration_in_millis // 1000

data_pipeline = Pipeline(name='ContinousMotionPipeline', steps=[
    MinMaxScaler(),
    Window(length=window_length_seconds, shift=0.3),
    SpectralFeatures(order=2)
])

"""
Enumerate features extracted from the SpectralFeatures step
"""
from pprint import pprint

pprint(data_pipeline['SpectralFeatures'][0].feature_names)

dataset.apply(data_pipeline)

dataset.describe()

#dataset.plot.features_pairplot(n=300)

"""
Perform classification with a RandomForest
"""
from everywhereml.sklearn.ensemble import RandomForestClassifier 

classifier = RandomForestClassifier(n_estimators=20, max_depth=20)
train, test = dataset.split(test_size=0.3)
classifier.fit(train)

print('Score on test set: %.2f' % classifier.score(test))

print(data_pipeline.to_arduino_file(
    'sketches/IMUClassify/Pipeline.h', 
    instance_name='pipeline'
))

print(classifier.to_arduino_file(
    'sketches/IMUClassify/Classifier.h', 
    instance_name='forest', 
    class_map=dataset.class_map
))