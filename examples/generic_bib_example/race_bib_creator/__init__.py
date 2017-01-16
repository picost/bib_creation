# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

The race_bib_creator package enables the creation of personnalized bibs for a
race. It is build around bib templates that are used to define a global bib sha
-pe.

Given a participant list, these templates can be used to create various person
-nalized bib designs in a modular and, hopefully, easy way.
"""

from .bib_factory import BibFactory
from .bib_template import BibTemplate