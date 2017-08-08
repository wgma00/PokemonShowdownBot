from plugins.math.Putnam import Putnam
from plugins.math.Putnam import LatexParsingException
import pytest


def test_putnam_problem_exception_handling():
    cmd = Putnam()
    # this example we can see everything should compile fine except at the end
    # we have not closed the \begin{itemize} case, so it will break on pdflatex
    with pytest.raises(LatexParsingException):
        cmd._upload_problem(
            (['\\documentclass[amssymb,twocolumn,pra,10pt,aps]{revtex4-1}', '\\usepackage{mathptmx,amsmath}', '',
              '\\begin{document}', '\\title{The Fiftieth Annual William Lowell Putnam Competition \\\\',
              'Saturday, December 2, 1989}', '\\maketitle', '', '\\begin{itemize}', '\\end{itemize}',
              '\\end{document}'],
             ['\\item[B--5]', 'Label the vertices of a trapezoid $T$ (quadrilateral with two parallel sides)',
              'inscribed in the unit circle as $A,\\,B,\\,C,\\,D$ so that $AB$ is parallel to',
              '$CD$ and $A,\\,B,\\,C,\\,D$ are in counterclockwise order. Let',
              '$s_1,\\,s_2$, and $d$ denote the lengths of the line segments',
              '$AB,\\, CD$, and $OE$, where E  is the point of intersection of the diagonals',
              'of $T$, and $O$ is the center of the circle. Determine the least upper bound of',
              '$\\frac{s_1-s_2}{d}$ over all such $T$ for which $d\\ne 0$, and describe all',
              'cases, if any, in which it is attained.',
              '\\begin{itemize}'])
        )
