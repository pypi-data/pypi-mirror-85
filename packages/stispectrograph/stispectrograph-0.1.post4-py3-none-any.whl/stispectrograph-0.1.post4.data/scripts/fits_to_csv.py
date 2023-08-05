#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re

from stispectrograph import Image, to_csv

fits_regex = re.compile(r"(.+)\.(FIT|fit)")

if len(sys.argv) in (2,3):
    cwd = False

    if len(sys.argv) == 2:
        path = os.getcwd()
        cwd = True
    else:
        path = sys.argv[2]
    if not os.path.isabs(path):
        path = os.path.join(os.getcwd(), path)

    try:
        mercury_line = int(sys.argv[1])
    except ValueError:
        print(f"\nError: Invalid mercury line pixel value: \"{sys.argv[1]}\"\n")
        sys.exit(2)

    if not os.path.exists(path):
        print(f"\nError: The path\"{path}\" does not exits.\n")
        sys.exit(2)

    if os.path.isfile(path):
        if (match := fits_regex.match(path)):
            try:
                image = Image(path)
            except Image.InvalidImageShapeError as e:
                print(f"\nError: File \"{path}\" has incorrect dimensions:")
                print(str(e)+"\n")
                sys.exit(1)
            data = image.get_spectral_data(mercury_line)
            to_csv(data, os.path.join(os.path.dirname(path), match.group(1)))
            print("Saved " + match.group(1) + ".csv")
        else:
            print(f"\nError: \"{path}\" is not a FITS file.\n")
            sys.exit(2)

    else:
        found = False
        for file in os.listdir(path):
            if (match := fits_regex.match(file)):
                file = os.path.join(path, file)
                found = True
                try:
                    image = Image(file)
                except Image.InvalidImageShapeError as e:
                    if cwd:
                        name = os.path.basename(file)
                    else:
                        name = file
                    print(f"\nError: File \"{name}\" has incorrect dimensions:")
                    print(str(e)+"\n")
                    continue
                data = image.get_spectral_data(mercury_line)
                to_csv(
                    data, os.path.join(path, match.group(1))
                    )
                print("Saved " + match.group(1) + ".csv")
        if not found:
            print(f"\nError: There are no FITS files in \"{path}\"\n")
            sys.exit(2)

    sys.exit(0)

elif len(sys.argv) == 1:
    print(f"\nUsage: {os.path.basename(sys.argv[0])} mercury_line_pixel \"[filename|directory]\"")
    print("Extracts spectral data from FITS files to csv.")
    print("The csv files are created in the same directory as the images, with the same names.")
    print("If a directory is specified, extracts data from all FITS files in that directory.")
    print("If a file is specified instead, extracts data from that file only.")
    print("If the last argument is ommited, defaults to the current working directory.\n")

else:
    print(f"\nError: Expected 1 or 2 arguments, got {len(sys.argv)-1}.")


