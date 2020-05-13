library("openxlsx")
library("aTSA")

data <- read.xlsx("hw12/quarterly.7775706_第一章.xlsx")
design <- na.omit(data[, c("Tbill", "r5", "r10")])

t_bill <- data.matrix(design["Tbill"])
r5 <- data.matrix(design["r5"])
r10 <- data.matrix(design["r10"])
r <- data.matrix(design[, c("r5", "r10")])

adf.test(t_bill)
adf.test(r5)
adf.test(r10)

coint.test(t_bill, r)