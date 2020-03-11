\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{homework}
\LoadClass[nobib]{tufte-handout}

% Load packages used often
\input{normal-packages.tex}

% Tweak tufte-handout if option `cn' enabled
\newif\if@tweaktufte %\@tweaktuftefalse
\DeclareOption{cn}{\@tweaktuftetrue}
\ProcessOptions\relax
\if@tweaktufte
  \input{tweak-tufte.tex}
  \RequirePackage{cleveref}
  \crefformat{equation}{式~(#2#1#3)}
\fi


% Lstlist setting
\RequirePackage{listings}
\RequirePackage{xcolor}
\definecolor{lbcolor}{rgb}{0.95,0.95,0.95} 
\lstset{
    basicstyle=\footnotesize\ttfamily,
    backgroundcolor=\color{lbcolor},
    xleftmargin=.1\textwidth, xrightmargin=.1\textwidth,
    autogobble
}
% `code' macro
\newcommand\code[1]{%
    \colorbox{lbcolor}{\lstinline{#1}}
}

% Subproblem environment
\newenvironment{subproblem}{\begin{enumerate}[leftmargin=0pt,label=(\roman*)]}{\end{enumerate}}

% Some useful math macros
\input{math-macros.tex}

% External author (.author.tex)
\if@tweaktufte
  \InputIfFileExists{.author.cn}{}{}
\else
  \InputIfFileExists{.author}{}{}
\fi