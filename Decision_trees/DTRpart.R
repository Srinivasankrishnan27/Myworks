
library(rpart)
mydata<-read.csv("trialPromoResults.csv")
xdata<-mydata[,2:11]
fit <- rpart(decision~., data=xdata)
summary(fit)
predictions <- predict(fit, data=xdata, type="class")
table(predictions, xdata$decision)
fix(xdata)
