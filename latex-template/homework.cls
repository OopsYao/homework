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
  \crefformat{table}{表~#2#1#3}
  \crefformat{figure}{图~#2#1#3}
\fi


% Lstlist setting
\RequirePackage{listings}
\RequirePackage{xcolor}
\definecolor{lbcolor}{rgb}{0.98,0.98,0.98} 
\lstset{
    basicstyle=\footnotesize\ttfamily,
    backgroundcolor=\color{lbcolor},
    % xleftmargin=.1\textwidth, xrightmargin=.1\textwidth,
    autogobble,
    breaklines=true,
    postbreak=\mbox{\textcolor{red}{$\hookrightarrow$}\space}
}
% `code' macro
\newcommand\code[1]{%
    \colorbox{lbcolor}{\lstinline{#1}}
}

% Problem
\newcounter{problem}
\if@tweaktufte
  \newcommand{\problem}[1][题\theproblem]{\stepcounter{problem}\section{#1}}
\else
  \newcommand{\problem}{\refstepcounter{problem}\section{Problem \theproblem}}
\fi
\counterwithin{equation}{problem}
\newcommand{\skipproblem}{\stepcounter{problem}}

% Subproblem environment
\newenvironment{subproblem}%
[1][(\roman*)]%
{\begin{enumerate}[leftmargin=0pt,label=#1]}%
{\end{enumerate}}

% Some useful math macros
\input{math-macros.tex}

% External author (.author.tex)
\if@tweaktufte
  \InputIfFileExists{.author.cn}{}{}
\else
  \InputIfFileExists{.author}{}{}
\fi