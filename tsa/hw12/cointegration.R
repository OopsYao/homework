library("openxlsx")
library("aTSA")

data <- read.xlsx("hw12/quarterly.7775706_第一章.xlsx")
design <- na.omit(data[, c("Tbill", "r5", "r10")])

t_bill <- data.matrix(design["Tbill"])
r <- data.matrix(design[, c("r5", "r10")])

coint.test(t_bill, r)