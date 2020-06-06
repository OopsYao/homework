library(openxlsx)

data <- read.xlsx("hw12/quarterly.7775706_第一章.xlsx")
target <- na.omit(data[, c("r10", "Tbill", "IndProd", "Unemp")])
print(target)