# Generates Latex code that can be processed with pdflatex
# to create a .pdf file that depicts Sierpinski triangle,
# obtained from Pascal triangle by drawing a black square
# when the corresponding number is odd.
# Uses a particular case of Luca's theorem which states that
# the number of ways of choosing k objects out of n is odd iff
# all digits in the binary representation of k are digits in the
# binary representation of n.
#
# Written by Eric Martin for COMP9021


dim = 128

latex_file = open('Sierpinski_triangle.tex', 'w')
print('\\documentclass[10pt]{article}\n'
      '\\usepackage{tikz}\n'
      '\\pagestyle{empty}\n'
      '\n'
      '\\begin{document}\n'
      '\n'
      '\\vspace*{\\fill}\n'
      '\\begin{center}\n'
      '\\begin{tikzpicture}[scale=0.047]\n', file = latex_file)
for n in range(dim):
    for k in range(n + 1):
        if k | n == n:
            print('\\fill({},{}) rectangle({},{});'.format(2 * k - n, -(2 * n), 2 * k - n + 2, -(2 * n) + 2), file = latex_file)
print('\\end{tikzpicture}\n'
      '\\end{center}\n'
      '\\vspace*{\\fill}\n'
      '\n'
      '\\end{document}\n', file = latex_file)
latex_file.close()
