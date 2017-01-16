# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 07:40:07 2016
@author: Pierre_COSTINI

This module contains the defintion of the `BibTemplate` class. A template is a
basis for the creation of a series of personnalized bibs for one or several
races.
As such, it can be used by one or more factories (`BibFactory` instances) to
create bibs.

The template defines how the bibs will look like through the base file (usually
a svg file created with Inkscape) and does all the work of personnalization
according to the information provided by the factory (when the `make_svg_file`
method is called) to create a given bib. It can also provide the command to
call Inkscape to convert the svg file it produces to a more widely usable png
file, especially to print the bibs. The command to call Inkscape (computer
dependant) has to be specified when the template is instanciated.

A typical shape for this command is::

    "C:\Program Files\Inkscape\inkscape.exe" -z -f {source_svg} -w {width} -j -e {dest_png}\n

Only the location of Inkscape has to be updated. The arguments passed to it (in
the braces) must be left unchanged. Their values are specified in the call to
the `make_conversion_command` method.
This is not very general and may be unconvenient.
However, this capabilty is just provided as an helper and still has to be
developped. Writting a script for conversion automation using another
software should not be an issue.

:Nota:

    Looking for an Inkscaoe installation and suggesting a command in an
    automated way would be a possible improvement.

Example
-------

>>> import race_bib_creator
>>> # Creating the template Instance
>>> template = race_bib_creator.BibTemplate(base_file_name=('bib_template_example.svg'),
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
>>> # Creating a factory for Race 1
>>> factory = race_bib_creator.BibFactory(participants="race_1\\participants_1.xlsx",
                                      field_for_numbering='Number')
>>> factory_2 = race_bib_creator.BibFactory(participants="race_2\\participants_2.xlsx",
                                      field_for_numbering='Number')
>>> # Creating bibs according to the template for race 1
>>> factory.make_bib_files(template,'race_1')
>>> # Creating bibs according to the template for race 1
>>> factory_2.make_bib_files(template,'race_2')

Class definition
----------------
"""
import os
import math
import warnings

class BibTemplate():
    """A template for personnalized runner id (bib) creation.

    :Attributes:
        **_base_file**: str
             Name of the file used as template for the bib. Personalized bibs
             can then be created according to this template by filling certain
             fields with specified values.
        **_fields**: dic
            Dictionnary which keys are strings containing fields names and
            values are strings containing "markers" for these fields in the
            base svg file. For personnalized bib creation, markers will be
            searched in the file and replaced by specified values.
        **_use_barcodes**: bool
            Specifies whether barcodes are used in this template or not.
        **_barcode_number_field_**: str
            Field where the barcode number is given.
        **_barcode_field_name**: str
            Field where the barcode marker is given.
        **_barcode_string_template**: str
            String template for barcode (content) creation.
        **_barcode_encoding**: str
            Type of barcode produced. Usable barcode types are those provided
            by pyBarcode package.
        **_id_ndigits_for_barcode**: int
            Number of digits to be used in the barcode id
        **_barcode_prefix_name**: str
            Prefix names for created barcode png files
        **_conversion_command**: str
            Command used to call Inkscape.
            A typical shape for this command is::

            "C:\Program Files\Inkscape\inkscape.exe" -z -f {source_svg} -w {width} -j -e {dest_png}\n

        **_output_file_path**: str
            Attribute used to store (temporarily) the output file path so
            that it can be used for command creation.

    """
    def __init__(self,base_file_name, fields, conversion_command=None,
                 use_barcodes=False, barcode_string_template="00{}",
                 barcode_encoding="code39", barcode_field_name = "barcode",
                 barcode_number_field_name="numero",
                 id_ndigits_for_barcode=5, barcode_prefix_name="barcode_"):
        """Returns a BibTemplate instance for runner id generation.

        :Parameters:

            *base_file_name*: str
                Name of the file used as template for the bib. Personalized bibs
                can then be created according to this template by filling certain
                fields with specified values.
            *fields*: dic
                Dictionnary which keys are strings containing fields names and
                values are strings containing "markers" for these fields in the
                base svg file. For personnalized bib creation, markers will be sea
                -rched in the file and replaced by specified values.
            *conversion_command*: str, optional
                Template command to be used if the creation of a script converting
                svg files to another format is requested. Right now, this functio
                -nality is very basi and only Inkscape can be used for that so a
                string to be formated as in the code hereunder is expected. This is
                to be improved.
            *use_barcodes*: bool, optional
                Specifies whether barcodes are used in this template or not.
            *barcode_string_template*: str, optional
                String template to be used for barcode creation. This string will
                be formated with another string of specified length containing the
                id of the bib for each new created bib.
            *barcode_encoding*: str, optional
                Encoding to be used for barcode creation. See pyBarcode
                documentation for more details.
                Default value is code39 which should be generic enough provided
                the number of digits is big enought (5 is suitable). A 6th
                digit (number or letter), a verification key, is added when the
                barcode is created.
            *barcode_number_field_name*: str, optional
                Name of the field specifying the number to be used to genrate the
                barcode. (bib bumber usually)
            *barcode_field_name*: str, optional
                Name of the field which specifies the marker for the barcode file.
            *id_ndigits_for_barcode*: int, optional
                Number of digits used in the barcode id in the barcode (fixed
                length with zero completion).
            *barcode_prefix_name*: str, optional
                Prefix for the name of the barcode files that may be generated.

        :Example:

            >>> # Creating a first template instance
            >>> template = race_bib_creator.BibTemplate(
                    'test_tt_2016\\dossard_patern_barcode.svg', {'numero':'DNB',
                    'barcode':'ean13.png','cat':"&lt;cat&gt;", 'prenom':"Ignace"},
                    use_barcodes=True)

            >>> # Creating a second template instance
            >>> template_2 = race_bib_creator.BibTemplate(
                    'test_tt_2016\\dossard_patern_no_barcode.svg', {'numero':'DNB',
                    'nom':'Goret', 'cat':"&lt;cat&gt;", 'prenom':"Ignace"},
                    use_barcodes=False)
        """
        assert isinstance(base_file_name,str), ("The name of the file used as "
        "template must hace type str")
        assert isinstance(fields,dict), ("The fields mus be given in a dict"
        " which keys are fields names (as in participants file) and values are"
        " fields marker in the base file.")
        assert (isinstance(conversion_command,str) or
                conversion_command is None), ("The conversion command must"
                " have type str.")
        assert isinstance(use_barcodes,bool), ("use_barcodes must have type "
        "bool")
        self._base_file = base_file_name
        self._fields = fields
        inkscape_dft_cmd = ('"C:\Program Files\Inkscape\inkscape.exe" '
            '-z -f {source_svg} -w {width} -j -e {dest_png}\n')
        self._conversion_command = conversion_command or inkscape_dft_cmd
        # whether to use a barcode or not
        self._use_barcodes = use_barcodes
        # field where the barcode number is given
        self._barcode_number_field_name = barcode_number_field_name
        # field where the barcode marker is given
        self._barcode_field_name = barcode_field_name
        # string template for barcode (content) creation
        self._barcode_string_template = barcode_string_template
        # type of barcode produced
        self._barcode_encoding = barcode_encoding
        # number of digits to be used in the barcode id
        self._id_ndigits_for_barcode = id_ndigits_for_barcode
        # prefix names for barcode png files
        # attribute used to store the output file path so that it can be used
        # for command creation
        self._barcode_prefix_name = barcode_prefix_name
        self._output_file_path = None

    def make_svg_file(self, fields_values, output_name, output_rep=None,
                      barcode_id=None):
        """Replaces the provided fields markers by provided fields values and
        returns output file name.


        :Parameters:

            *fields_values*: dic
                Dictionnary of values of the various fields to be personnalized in
                the resulting svg file. Keys are fields names and values are fields
                contents as should appear on the bib that is beeing created.
            *output_name*: str
                Name of the resulting svg file that will be created by  the method.
            *output_rep*: str, optional
                path toward the repository in which the output file must be created.
            *barcode_id*: int, optional
                Number to be passed to the barcode creator if no field provides it.

        :Returns:

            *bib*: str
                Path toward the output svg file, relative if the provided path
                toward the output repertory is relative, absolute if it is
                absolute.

        :Info:

            The way this task is done is currently very rough and inefficient
            (see source code): the markers are looked for and replaced if found
            in all the lines of the file for each new bib...
            Using acleaner method, e.g. using a dedicated templating package
            should be (and is) considered as improvement to this code.

        .. warning::
             For now, if pictures are referenced in the svg basefile, they
             must be present in the output repository because they will also
             be referenced in the results files with the same path as in the
             initial file (relative path + absolute path as back-up).

        """
        if output_rep is None:
            output_rep = os.getcwd()
        # Barcode file creation if needed
        if self._use_barcodes:
            try:
                number = fields_values[self._barcode_number_field_name]
            except AttributeError:
                if barcode_id is not None:
                    number = barcode_id
                else:
                    print("There is no {} field to be used for the barcode in"
                          " the provided "
                          "inputs".format(self._barcode_number_field_name))
                    return()
            barcode_file = self._make_barcode(number,output_rep)
            fields_values[self._barcode_field_name] = barcode_file
        #selecting provided field values that will be used
        fields_to_use = []
        for field in fields_values.keys():
            if self._fields.get(field) is not None:
                fields_to_use.append(field)
        # Opening the template file (svg file or other text parsable file)
        # TODO: cette partie est degueu. Utiliser une gestion de template exi
        # -stant (ex. jinja2 mais pas de support de Python 3.5 pour l'instant)
        with open(self._base_file,'r') as template:
            line = template.readline()
            # Opening output file
            bib = output_rep + '\\' + output_name
            with open(bib,'w') as output:
                while line:
                    for field in fields_to_use:
                        line = line.replace(self._fields[field],
                                            str(fields_values[field]))
                    output.write(line)
                    line = template.readline()
                # Reading template file and replacing fields
                # Closing output file
                output.close()
            # Closing the template file
            template.close()
        self._output_file_path = bib
        #/!\ For now, if pictures are referenced in the svg basefile, they
        # must be present in the output repository because they will also
        # be referenced in the results files.
        return(bib)

    def make_conversion_command(self,source=None,dest=None,px_width=1000):
        """Returns the conversion command from svg to png by Inkscape. See
        Inkscape documentation.


       :Parameters:

            *source*: str, optional
                path toward svg file to convert.
            *dest*: str, optional
                path toward location of the expected result png file.
            *px_width*: int, optional
                Width of the resulting png picture in px.

        :Returns:

            *command*: str
                Command to make a png from the given source file using
                Inkscape.

        """
        assert isinstance(px_width,int), "The number of px must be an integer."
        source = source or self._output_file_path
        source = os.path.abspath(source)
        dest = dest or self._output_file_path[:-3]+'png'
        dest = os.path.abspath(dest)
        command = self._conversion_command.format(**{'source_svg':source,
                                                   'width':px_width,
                                                   'dest_png':dest})
        return(command)

    def _make_barcode(self, number, output_rep):
        """Creates a barcode picture and returns the file name.


        :Parameters:

            *number*: int
                Id. number of the participant for which the barcode is generat
                -ed.
            *output_rep*: str
                Path toward the repository in which the output barcode file
                must be produced.

        :Info:

            The actual string that will be passed to the barcode maker is composed
            of a string created by the method, inserted in self._barcode_string_tem
            -plate. The created string is the number passed to this method, comple
            -mented with zeros as prefix so that its lenght is equal to
            self._id_ndigits_for_barcode.
            This enables to have fixed length strings, more easily usable when
            scanning the barcodes.

        """
        import barcode
        from barcode.writer import ImageWriter
        #create the string to be encoded
        # TODO: retravailler pour rendre plus général
        number_ndigits = int(math.log10(number)) + 1
        # Give a warnong if the number is too long
        if number_ndigits > self._id_ndigits_for_barcode:
            warnings.warn("Not enough digits attributed to IDs given "
                          "participants numbers: {} has {} digits but {} are"
                          " expected at most".format(number,number_ndigits,
                          self._id_ndigits_for_barcode))
        barcode_string_complement =  "0" * (self._id_ndigits_for_barcode -
                                            number_ndigits) + str(number)
        barcode_string = self._barcode_string_template.format(
                            barcode_string_complement)
        #create the barcode png picture
        barcode_png = str.join("",[self._barcode_prefix_name, barcode_string])
        barcode_instance = barcode.get(self._barcode_encoding,
                                       barcode_string,
                                       writer=ImageWriter())
        barcode_file_path = output_rep + '\\' + barcode_png
        barcode_instance.save(barcode_file_path)
        return(barcode_png+'.png')


#if __name__ == '__main__':
#    import doctest
#    doctest.testmod()
#    template =  BibTemplate('dossard_patern_barcode.svg',{'numero':'DNB',
#                                                          'barcode':'ean13.png'},
#                               use_barcodes=True)
#    fields_values = {'numero':12}
#    template.make_svg_file(fields_values,'test_svg.svg')