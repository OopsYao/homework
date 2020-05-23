# Homework of Stochastic Differential Equation

> 📖 My homework of SDE

File `.author.tex`  which defines
`\author` is ignored for privacy matter.

# TODOs
- [ ] `wrapper.tex` for single homework.
  
  Based on `\jobname` to determine whether it is a single compile
  or batch one.

  Single compile mode is for dev and batch for prodution.
  Then every `main.tex` in subdir can be substructed
  as a tex segment which is more friendly to merge.

- [ ] Preserve title information of sub `main.tex` (by `\jobname`
  and str manipulation?)