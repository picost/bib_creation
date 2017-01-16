# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 2016

Ce script illustre comment plusieurs templates de dossards différents peuvent
être utilisés avec la même liste de participants pour créer des dossards distin
-cts personnalisés avec ou sans codes-barres.

@author: Pierre_COSTINI
"""
import race_bib_creator

# Création d'un premier objet template
template = race_bib_creator.BibTemplate(base_file_name=('test_tt_2016\\dossard'
                                                        '_patern_barcode.svg'),
                                        fields={'numero':'DNB',
                                                'barcode':'ean13.png',
                                                'cat':"&lt;cat&gt;",
                                                'prenom':"Ignace"},
                                        use_barcodes=True)

# Création d'un second objet template
template_2 = race_bib_creator.BibTemplate(base_file_name=('test_tt_2016\\dossa'
                                                          'rd_patern_no_barcod'
                                                          'e.svg'),
                                          fields={'numero':'DNB','nom':'Goret',
                                                  'cat':"&lt;cat&gt;",
                                                  'prenom':"Ignace"},
                                          use_barcodes=False)

# création de la factory associée à la liste de participants
factory = race_bib_creator.BibFactory(participants="test_tt_2016\\test.xlsx",
                                      field_for_numbering='numero')

# Création des dossards selon le premier template
factory.make_bib_files(template,'test_tt_2016\\resultats')
# Création des dossards selon le second template
factory.make_bib_files(template_2,'test_tt_2016\\resultats_2')