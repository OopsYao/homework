library(openxlsx)
library(ggplot2)

data <- read.xlsx("hw12/quarterly.7775706_第一章.xlsx")
design <- na.omit(data[, c("Tbill", "r5", "r10")])

t_bill <- data.matrix(design["Tbill"])
r5 <- data.matrix(design["r5"])
r10 <- data.matrix(design["r10"])
r <- data.matrix(design[, c("r5", "r10")])

index <- seq_len(nrow(design))
ggplot(data.frame(index, design)) +
    geom_point(aes(index, r5)) +
    geom_point(aes(index, r10))

# ADF test for the 3 sequences
adf.test(t_bill)
adf.test(r5)
adf.test(r10)

# Direct regression
coint_lm <- lm(t_bill ~ r5 + r10)
coint_res <- resid(coint_lm)

# ADF test of residual
adf.test(coint_res)
# plot(coint_res, main = "Residual of Regression", pch = 19, frame = FALSE)
