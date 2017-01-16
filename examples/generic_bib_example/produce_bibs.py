# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 13:59:18 2017

@author: Pierre_COSTINI
"""

import race_bib_creator

# Creating the template Instance
template = race_bib_creator.BibTemplate(base_file_name=('bib_template_example.svg'),
                                        fields={'Number':'DNB',
                                                'barcode':'barcode.png',
                                                'Category':'&lt;cat&gt;',
                                                'Firstname':'first_name',
                                                'Date':'event_date',
                                                'Race':'event_name'},
                                        barcode_number_field_name='Number',
                                        barcode_string_template='00{}',
                                        barcode_encoding='code39',
                                        barcode_field_name='barcode',
                                        id_ndigits_for_barcode=5,
                                        barcode_prefix_name='barcode_file',
                                        use_barcodes=True)


# Creating a factory for Race 1
factory = race_bib_creator.BibFactory(participants="race_1\\participants_1.xlsx",
                                      field_for_numbering='Number')

factory_2 = race_bib_creator.BibFactory(participants="race_2\\participants_2.xlsx",
                                      field_for_numbering='Number')

# Creating bibs according to the template for race 1
factory.make_bib_files(template,'race_1')
# Creating bibs according to the template for race 1
factory_2.make_bib_files(template,'race_2')