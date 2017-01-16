How to use this code to create my bibs?
=======================================

Use the provided examples
-------------------------

First: RTFM. But if you read this text, you are probably from the clear side of
the Force.

Then, the examples provided in the previous sections and those distributed
with the package should be enough for you to get a good idea of how this
code works and should be used for various purposes.
Take a look at the `illustrations` folder if you need to see how a svg file
used in the examples looks like.

Finally, the code of this package should be understandable for someone
who knows a little about python as it only uses very basic capabilities of the
language. You should therfore be able to adapt the code to your needs without
to much effort.


Make sure you have the right packages and softwares
----------------------------------------------------

This code was written using the following packages:
    - pyBarcode v0.7
    - pandas v0.18.1

Inkscape v0.91 was used to create the svg template files and transform the svg
files to pngs.

Troubleshooting
---------------

The present code is a very first basic implementation of bib creation
capabilities.
As such, it lacks robustness to various changes in the way it is
used.
For examples, the following issues are known but not corrected yet:

    1. Special caracters in the participants tables may produce bad results or
    Errors. It is recommanded that one sticks to "basic" ascii caracter, which
    can be done by a simple post-processing of the input data.

    2. Empty cells in the participants table my produce errors or bad results.
    If an issue related to empty cells in theses tables arises, try to fill the
    empty cells with a blanc (' ').

    3. Be carefull with the type of data provided in the Excel sheets. If the
    data doesn't have the expected type, bad results or errors may arise. E.g.:

        - The field used for barcode numbering is not an integer (or alike):
          the barcode creation will fail.

        - A field has a date format in Excel: the text written in the bib will
          contain the date **and** the time (00:00:00).
