# Homework of Stochastic Differential Equation

> 📖 My homework of SDE

This is a repository that contains the source code of 
my SDE course.

File `.author.tex`  which defines
`\author` is ignored for privacy matter.

## Before build

Make sure TeX path contains directory `latex-template`
which contains the `.sty` files used for this project.
To this end, we can change the `TEXINPUTS` environment
variable. e.g. under Unix OS,
```
export TEXINPUTS="latex-template:"
```

## How to build

Simply, a single line of command.
```bash
latexmk -pdf main
```

### How to build separately

Without building it as a whole bundle,
we can build it as individual files of each homework.

First change the num in the file `wrapper.tex`,
then `latexmk -pdf wrapper`.