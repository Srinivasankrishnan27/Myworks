# Bagging CART in RR
# load the package
library(ipred)
# load data
set.seed(301)
mydata<-read.csv("smoteddata.csv.csv")
mydata<-read.xlsx2("smoteddata_1.xls",1)
xlsx.read()
rcount=nrow(mydata)
train_rcount=round(rcount*(0.70))
trainsample=sample(rcount,train_rcount)
xdata<-mydata[,2:11]
# Load the shuffled  training & Testing data set from the Data frame
Train=xdata[trainsample,]
Test=xdata[-trainsample,]
# fit model
fit <- bagging(X..decision.~., data=Train)
# summarize the fit
summary(fit)
# make predictions
predictions <- predict(fit, Test, type="class")
# summarize accuracy
table(Test$X..decision.,predictions)

