#!/usr/bin/env python
# script to create mosaic from several tiles of MODIS
#
#  (c) Copyright Luca Delucchi 2012
#  Authors: Luca Delucchi
#  Email: luca dot delucchi at iasma dot it
#
##################################################################
#
#  This MODIS Python script is licensed under the terms of GNU GPL 2.
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as
#  published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#  See the GNU General Public License for more details.
#
##################################################################

#import system library
import os
import sys
import string
from types import ListType
#import modis library
from pymodis import convertmodis, optparse_gui, optparse_required

ERROR = "You have to define the name of a text file containing HDF files." \
        " (One HDF file for line)"


def main():
    """Main function"""
    #usage
    usage = "usage: %prog [options] hdflist_file"
    if 1 == len(sys.argv):
        option_parser_class = optparse_gui.OptionParser
    else:
        option_parser_class = optparse_required.OptionParser
    parser = option_parser_class(usage=usage, description='modis_mosaic')
    #spatial extent
    #mrt path
    parser.add_option("-m", "--mrt", dest="mrt_path", required=True,
                      help="the path to MRT software", metavar="MRT_PATH",
                      type='directory')
    parser.add_option("-o", "--output", dest="output", required=True,
                      help="the name of output mosaic", metavar="OUTPUT_FILE")
    #write into file
    parser.add_option("-s", "--subset", dest="subset",
                      help="a subset of product layers. The string should" \
                      " be similar to: 1 0 [default: all layers]")

    (options, args) = parser.parse_args()

    #check the number of tiles
    if not args:
        print ERROR
        sys.exit()
    else:
        if type(args) != ListType:
            print ERROR
            sys.exit()
        elif len(args) > 1:
            print ERROR
            sys.exit()

    if not os.path.isfile(args[0]):
        parser.error("You have to define the name of a text file containing HDF " \
                     "files. (One HDF file for line)")

    #check is a subset it is set
    if not options.subset:
        options.subset = False
    else:
        if string.find(options.subset, '(') != -1 or string.find(options.subset, ')') != -1:
            parser.error('ERROR: The spectral string should be similar to: "1 0"')

    modisOgg = convertmodis.createMosaic(args[0], options.output,
                                         options.mrt_path,  options.subset)
    modisOgg.run()

#add options
if __name__ == "__main__":
    main()
