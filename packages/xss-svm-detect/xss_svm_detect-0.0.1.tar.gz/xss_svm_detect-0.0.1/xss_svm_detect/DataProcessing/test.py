from DataProcessing.DataProcessor import DataProcessor

# 5 here means the minimum length of each sentences
dataProcessor = DataProcessor(5)
# X is the [The number of entries * The length of each entry] input list
# Y is the [The number of entries * 1] label list
X, Y = dataProcessor.dataProcessingForRNN("xss-20000.txt", "labeled_data.csv")
X, Y = dataProcessor.dataProcessingForSVM("xss-20000.txt", "labeled_data.csv")
print(len(X[0]))
print(len(X))

