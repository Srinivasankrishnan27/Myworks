# load the package
library(C50)
# load data
set.seed(200)
mydata<-read.csv("KNN2.csv")
Test<-read.csv("custdatabase.csv")
Valdata<-read.csv("Cust_Actual.csv")
xdata<-mydata[,2:11]
Test<-Test[,2:11]
# fit model
#fit <- C5.0(decision~., data=Train, trials=10,)
fit<- C5.0(decision ~.,data = xdata,trials = 10, control = C5.0Control(CF = 0.99))
# summarize the fit
print(fit)
# make predictions
predictions <- predict(fit, Test)
# summarize accuracy
table(Valdata$status,predictions)
table(true=Valdata$status, predicted=predictions)
result<- cbind(Valdata, data.frame(predictions))
#write.csv(result, file="G:\\Sem 2\\IS\\2b\\results.csv")
result.size = nrow(result)
result.correct = nrow(result[(result$predictions) == result$status,])
cat("Total No.Of records = ",result.size,"\n")
cat("Correct predictions = ", result.correct ,"\n")
cat("Accuracy = ", result.correct / result.size * 100 ,"\n")
