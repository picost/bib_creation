# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 11:54:00 2016
@author: Pierre_COSTINI

This module contains the definition of the `BibFactory` class that implements
bib factories.
Bib factories are object that enable you to create personnalized bibs for a
race starting from a table of participants and one or more bib templates. This
lets you try easily different designs for your bibs, showing runners' names,
teams, using barcodes or not etc.

Example
-------

The following code illustrates how a bib factory is instanciated and used with
two different bib templates to create two sets of bibs, one with barcodes, the
other without.

>>> import race_bib_creator
>>> # Creating a first bib template
>>> template = race_bib_creator.BibTemplate(base_file_name=('test_tt_2016\\dossard'
                                                        '_patern_barcode.svg'),
                                        fields={'numero':'DNB',
                                                'barcode':'ean13.png',
                                                'cat':"&lt;cat&gt;",
                                                'prenom':"Ignace"},
                                        use_barcodes=True)
>>> # Creating a second bib template that doesn't use barcodes.
>>> template_2 = race_bib_creator.BibTemplate(base_file_name=('test_tt_2016\\dossa'
                                                          'rd_patern_no_barcod'
                                                          'e.svg'),
                                          fields={'numero':'DNB','nom':'Goret',
                                                  'cat':"&lt;cat&gt;",
                                                  'prenom':"Ignace"},
                                          use_barcodes=False)

>>> # Creating a factory associated with the list of participants
>>> factory = race_bib_creator.BibFactory(participants="test_tt_2016\\test.xlsx",
                                      field_for_numbering='numero')
>>> # Creating bibs according to the first template
>>> factory.make_bib_files(template,'test_tt_2016\\resultats')
>>> # Creating bibs according to the second template
>>> factory.make_bib_files(template_2,'test_tt_2016\\resultats_2')

Class definition
----------------
"""
import pandas as pd
import os

class BibFactory():
    """
    A Bibfactory object is instanciated starting from a participants list.
    This "list" is a table containing all the information about the
    participants to your race. This table will be used by the factory to
    provide information to `BibTemplate` objects in order to personnlize the
    bibs.

    :Attributes:

        **participants**: pd.DataFrame
            Table containing the information about the participants to the race.
            The columns names are the fields names that will be provided to the
            BibTemplate method that create individual bibs.
        **_bib_template**: BibTemplate, optional
            The bib template currently attached to the factory.
        **_field_for_numbering**: str, optional
            Name of the (integer) field (column of `self.participants`) used as
            unique identifier for the runners, and therefore, as bib number.
        **_output_rep**: str, optional
            Path toward the repository where the bib files will be stored.
        **_output_file_prefix**: str, optional
            Prefix for the name of the output bib files that will be produced by
            the factory. This prefix will be complemented with the bib number.


    :Methods:

    """
    def __init__(self, participants, bib_template=None,
                 field_for_numbering=None, output_rep=None,
                 output_file_prefix="dossard_"):
        """Create an instance of bib factory for a given participant lists. To
        be used with various bib templates.

        """
        self._bib_template = bib_template
        self.participants = pd.read_excel(participants)
        self._output_rep = output_rep or os.getcwd()
        self._field_for_numbering = field_for_numbering
        self._output_file_prefix = output_file_prefix

    def make_bib_files(self,bib_template=None, output_rep=None,
                       script_name=None, output_file_prefix=None,
                       make_convert_script=True, png_px_width=2000):
        """Creates a svg file containing the bib for each participant.
        Returns the output repository.

        :Parameters:

            *bib_template*: BibTemplate, optional
                The bib template to be used for bib creation and attached to
                the factory.
                If no template is provided, the template attached to the
                factory is used if one is available. Else, the method fails.
            *output_rep*: str, optional
                Path toward the repository where the bib files will be stored.
            *output_file_prefix*: str, optional
                Prefix for the name of the output bib files that will be
                produced by the factory. This prefix will be complemented with
                the bib number
            *make_convert_script*: bool, optional
                Specifies whether a script to convert the svg files to pngs
                with Inkscape is created with the bibs. Default is True which
                means that a `make_pngs.bat` script is written in the output
                repertory that, if executed, calls inkscape to convert the
                resulting svg fils to pngs. The command to call Inkscape is
                specified in the BibTemplate object used.
            *png_px_width*: int
                Number of px to be used as width for the png production. Used
                if `make_convert_script` is `True`. See `BibTemplate`
                documentation. Default value is 2000. This may produce
                big-sized files but ensures barcodes are well printed enough if
                directly printed on the bib.

            The parameters provided to this method are used to set the values
            of the associated (private) attributes.

        :Returns:

            *output_rep*: str
                Output repository where the resulting fils are stored.

        .. see-also:

            Module: :py:mod: `bib_template`
        """
        if bib_template is None:
            bib_template = self._bib_template
        else:
            self._bib_template = bib_template
        if output_file_prefix is not None:
            self._output_file_prefix = output_file_prefix
        if output_rep is not None:
            self._output_rep = output_rep
        if make_convert_script:
            script_name = script_name or "make_pngs.bat"
            script = open(self._output_rep+'\\'+script_name,"w")
        try:
            for index,row in self.participants.iterrows():
                if self._field_for_numbering is None:
                    number = index + 1
                else:
                    number = row[self._field_for_numbering]
                output_name = self._output_file_prefix + str(number) + '.svg'
                self._bib_template.make_svg_file(row, output_name,
                                                 output_rep=self._output_rep)
                if make_convert_script:
                    command = self._bib_template.make_conversion_command()
                    script.write(command)
        except AttributeError:
            if make_convert_script:
                script.close()
                print("closed")
            raise
        if make_convert_script:
            script.close()
            print("closed")
        return(self._output_rep)

#    def


if __name__ == '__main__':
    from dossard_template import BibTemplate
    template =  BibTemplate('dossard_patern_barcode.svg',{'numero':'DNB',
                                                          'barcode':'ean13.png',
                                                          'cat':"&lt;cat&gt;",
                                                          'prenom':"Ignace"},
                               use_barcodes=True)
    factory = BibFactory(participants="test.xlsx",field_for_numbering='numero')
    factory.make_bib_files(template,'test_out')