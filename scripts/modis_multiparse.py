#!/usr/bin/env python
# script to obtain the bounding box of several tiles and write xml file of the mosaic
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
import sys
#import modis library
from pymodis import parsemodis, optparse_gui, optparse_required


def readDict(dic):
    """Function to decode dictionary"""
    out = ""
    for k, v in dic.iteritems():
        out += "%s = %s\n" % (k, v)
    return out


def main():
    """Main function"""
    #usage
    usage = "usage: %prog [options] hdf_files_list"
    if 1 == len(sys.argv):
        option_parser_class = optparse_gui.OptionParser
    else:
        option_parser_class = optparse_required.OptionParser
    parser = option_parser_class(usage=usage, description='modis_multiparse')
    #spatial extent
    parser.add_option("-b", action="store_true", dest="bound", default=False,
                      help="print the values related to the spatial max extent")
    #write into file
    parser.add_option("-w", "--write", dest="output", metavar="OUTPUT_FILE",
                      help="write the MODIS XML metadata file for MODIS mosaic")

    (options, args) = parser.parse_args()
    #create modis object
    if len(args) < 2:
        parser.error("You have to define the name of HDF files")
    modisOgg = parsemodis.parseModisMulti(args)

    if options.bound:
        modisOgg.valBound()
        print readDict(modisOgg.boundary)
    elif options.output:
        modisOgg.writexml(options.output)
        print "%s write correctly" % options.output
    else:
        parser.error("You have to choose at least one option")

#add options
if __name__ == "__main__":
    main()
