# load the package
library(gbm)
# load data
mydata<-read.csv("trialPromoResults.csv")
rcount=nrow(mydata)
train_rcount=round(rcount*(0.75))
trainsample=sample(rcount,train_rcount)
xdata<-mydata[,2:11]
# Load the shuffled  training & Testing data set from the Data frame
Train=xdata[trainsample,]
Test=xdata[-trainsample,]
# fit model
fit <- gbm(decision~., data=Train, distribution="multinomial")
# summarize the fit
print(fit)
# make predictions
predictions <- predict(fit, Test)
# summarize accuracy
table(predictions, Test$decision)
