# load the package
library(randomForest)
# load data
set.seed(301)
mydata<-read.csv("smoteddata_modified.csv")
rcount=nrow(mydata)
train_rcount=round(rcount*(0.75))
trainsample=sample(rcount,train_rcount)
xdata<-mydata[,2:11]
# Load the shuffled  training & Testing data set from the Data frame
Train=xdata[trainsample,]
Test=xdata[-trainsample,]
# fit model
fit <- randomForest(decision~., data=Train)
# summarize the fit
summary(fit)
# make predictions
predictions <- predict(fit, Test)
# summarize accuracy
table(Test$decision,predictions)

