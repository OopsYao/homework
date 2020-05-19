library(openxlsx)
library(ggplot2)
library(aTSA)

data <- read.xlsx("hw12/quarterly.7775706_第一章.xlsx")
design <- na.omit(data[, c("Tbill", "r5", "r10")])

t_bill <- data.matrix(design["Tbill"])
r5 <- data.matrix(design["r5"])
r10 <- data.matrix(design["r10"])

index <- seq_len(nrow(design))
ggplot(data.frame(index, design)) +
    geom_point(aes(index, r5), color = "blue") +
    geom_point(aes(index, r10), color = "green") +
    geom_point(aes(index, t_bill), color = "red")

# ADF test for the 3 sequences
adf.test(t_bill)
adf.test(r5)
adf.test(r10)

# Direct regression
coint_lm <- lm(t_bill ~ r5 + r10)
print(coint_lm)

# ADF test of residual
coint_res <- resid(coint_lm)
adf.test(coint_res)

# ECM
print(lm(diff(t_bill) ~ diff(r5) + diff(r10) + head(coint_res, -1) - 1))
# ECM by aTSA/ecm
# This leads a slightly different result
r <- data.matrix(design[, c("r5", "r10")])
ecm(t_bill, r)