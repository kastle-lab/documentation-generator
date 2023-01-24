# -*- coding: utf-8 -*-
"""PDF document generator

This module loades a panads dataframe and generates a PDF document using its columns.

# PDF Generation
"""

# pip install pylatex
# pip install pdflatex
# sudo apt-get install latexmk
# sudo apt-get install -y texlive-latex-extra

"""More information about the PDF generation:
https://jeltef.github.io/PyLaTeX/current/index.html
"""

import pandas as pd
from pylatex import Command, Document, Subsection
# from pylatex.section import *
from pylatex.basic import *
from pylatex.utils import NoEscape


def remove_newline(x):
  return " ".join(str(x).split())


def fill_document(doc, doc_df):
    for id, row in doc_df.iterrows():
      doc.append(NewPage())
      for column in doc_df.columns:
        with doc.create(Subsection(remove_newline(column), numbering=False)):
          if column != "FILTER":
            doc.append(MediumText(row[column]))
          else:
            doc.append(MediumText(remove_newline(row[column])))


if __name__ == '__main__':

    doc_df = pd.read_csv("documentation_df.csv")    
    geometry_options = {
      # "head": "40pt",
      "margin": "1.5in",
      # "bottom": "1in",
      # "includeheadfoot": True
    }
    doc = Document(geometry_options=geometry_options)

    doc.preamble.append(Command('title', 'KWG Documentation'))
    doc.preamble.append(Command('author', 'KWG Team'))
    # doc.preamble.append(Command('date', NoEscape(r'\today')))
    doc.preamble.append(Command('date', "2022"))
    doc.append(NoEscape(r'\maketitle'))

    fill_document(doc, doc_df)

    doc.generate_pdf('KWG_DOC', clean_tex=False)
    # tex = doc.dumps()  # The document as string in LaTeX syntax

