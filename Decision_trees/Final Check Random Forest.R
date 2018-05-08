# load the package
rm(list=ls())
require(nnet)
library(C50)
library(ipred)
library(randomForest)
library(rpart)
library(RWeka)
# load data
mydata<-read.csv("Smotedall1000_2_modified.csv")
testdata<-read.csv("custdatabase.csv")
Valdata<-read.csv("Cust_Actual.csv")
xdata<-mydata[,2:11]
fintestdata<-testdata[,2:10]
# fit model
# Random Forest
#fit <- randomForest(decision~., data=xdata) 
# Bagging
#fit <- bagging(decision~., data=xdata)
# GRAD Boost
#fit <- gbm(decision~., data=xdata, distribution="multinomial")
# CART
#fit <- J48(decision~., data=xdata)
# PART
#fit <- PART(decision~., data=xdata)
# C5.0
#fit <- C5.0(decision~., data=xdata, trials=100)
# Nnet
fit <- multinom(decision~., data=xdata)
#fit <- nnet(decision~., data=xdata, size=5, linout=TRUE, skip=TRUE, MaxNWts=10000, trace=FALSE, maxit=1000)
#fit <- nnet(decision~., data=xdata, size=5)
predictions <- predict(fit, fintestdata,type = "class")
# summarize the fit
summary(fit)
# make predictions
#predictions <- predict(fit, fintestdata)
# summarize accuracy
table(Valdata$status,predictions)
table(true=Valdata$status, predicted=predictions)
result<- cbind(Valdata, data.frame(predictions))
result.size = nrow(result)
result.correct = nrow(result[(result$predictions) == result$status,])
cat("Total No.Of records = ",result.size,"\n")
cat("Correct predictions = ", result.correct ,"\n")
cat("Accuracy = ", result.correct / result.size * 100 ,"\n")