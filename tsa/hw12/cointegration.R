library(openxlsx)
library(ggplot2)
library(aTSA)

data <- read.xlsx("hw12/quarterly.7775706_第一章.xlsx")
design <- na.omit(data[, c("Tbill", "r5", "r10")])

t_bill <- data.matrix(design["Tbill"])
r5 <- data.matrix(design["r5"])
r10 <- data.matrix(design["r10"])

# Visualization
data_refactor <- function(df, name) {
    idx <- seq_len(nrow(df))
    fr <- data.frame(idx, df, name)
    colnames(fr) <- c("idx", "val", "name")
    fr
}
df_grh <- rbind(
    data_refactor(t_bill, "tBill"),
    data_refactor(r5, "r5"),
    data_refactor(r10, "r10")
)
ggplot(df_grh) +
    geom_line(aes(idx, val, color = name))
ggsave("hw12/ts.pdf", width = 8, height = 5)

# ADF test for the 3 sequences
adf.test(t_bill)
adf.test(r5)
adf.test(r10)

# Direct regression
coint_lm <- lm(t_bill ~ r5 + r10)
print(coint_lm)

# ADF test of residual
coint_res <- resid(coint_lm)
df_res <- data.frame("index" = seq_len(length(coint_res)), coint_res)
ggplot(df_res) +
    geom_line(aes(index, coint_res))
ggsave("hw12/residual.pdf", width = 5, height = 5)
adf.test(coint_res)

# ECM
print(lm(diff(t_bill) ~ diff(r5) + diff(r10) + head(coint_res, -1) - 1))
# ECM by aTSA/ecm
# This leads a slightly different result
r <- data.matrix(design[, c("r5", "r10")])
ecm(t_bill, r)