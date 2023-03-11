clear
load('fulldata.mat');

sizeX = size(fall);
Nframe = sizeX(2);
for ind = 1:Nframe
  meantemp = mean(fall{ind});
  stdtemp = std(fall{ind});
  FallFeature1(ind, :) = meantemp(1:3);
  FallFeature2(ind, :) = stdtemp(1:3);
end

sizeX = size(NotFall);
Zframe = sizeX(2);
for ind = 1:Zframe
  meantemp = mean(NotFall{ind});
  stdtemp = std(NotFall{ind});
  NotFallFeature1(ind, :) = meantemp(1:3);
  NotFallFeature2(ind, :) = stdtemp(1:3);
end

X = [FallFeature1,FallFeature2;
    NotFallFeature1,NotFallFeature2];

Y = [ones(Nframe,1)*2;ones(Zframe,1)];

rng('default') % For reproducibility
Partition = cvpartition(Y,'Holdout',0.20);
trainingInds = training(Partition); % Indices for the training set
XTrain = X(trainingInds,:);
YTrain = Y(trainingInds);
testInds = test(Partition); % Indices for the test set
XTest = X(testInds,:);
YTest = Y(testInds);

template = templateTree(...
    'MaxNumSplits', 399);
ensMdl = fitcensemble(...
    XTrain, ...
    YTrain, ...
    'Method', 'Bag', ...
    'NumLearningCycles', 20, ...
    'Learners', template, ...
    'ClassNames', [1; 2; 3]);
%% Prediction accuracy

% Perform 5-fold cross-validation for classificationEnsemble and compute the validation accuracy.
partitionedModel = crossval(ensMdl,'KFold',5);

validationAccuracy = 1-kfoldLoss(partitionedModel)

%% Test data accuracy

% Evaluate performance of test data
testAccuracy = 1-loss(ensMdl,XTest,YTest)