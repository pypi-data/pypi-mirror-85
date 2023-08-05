=======DESCRIPTION=======
This software is meant to replace part of the functionality of
SBIG's "ST-i Spectroscopy Program" used with the ST-i spectrograph.
As of version 0.1, it can be used mainly to extract spectral data
from FITS files into csv files.

This software operates in Angstom for wavelength, as that is
what the "ST-i Spectroscopy Program" does.

======INSTALLATION=======
To install the package from PyPI run:
>>> pip install stispectrograph

To install the python package from the source distribution,
go to the stispectrograph directory and run:
>>> python setup.py install
THE WINDOWS EXECUTABLE IS NOT AVAILABLE FROM THE SOURCE
DISTROBUTION ON PyPI

The included windows executable can be used as-is.

==========GUIDE==========
In version 0.1, it consists of:
The python package "stispectrograph", which includes the script
"fits_to_csv.py", which will be installed as a command line tool
together with the package.

The script is also available as a standalone windows executable, "fits_to_csv.exe", 
but this is significantly slower than the python version,
especially when used with single FITS files.
This is recommended only if you do not have a python interpreter
installed on your computer.
As of now, only a windows executable is available, but the package itself,
and "fits_to_csv.py", is os-independent.


The executable can be used for basic extraction of data from a spectrograph image
into a csv file. It's used as a command line tool.¨

I recommend taking pictures using CCDops using the procedure given in the spectrograph manual.
This software will only accept images with dimensions 121x648 pixels, which in
CCDops means setting resolution to 1xN and vertical binning to 4.

First, you need to know on what pixel x-value the 5461 Å mercury line appears in your images.
This depends on the calibration process.
Consult the spectrograph manual for how to identify this line.

Then run the script like so:
>>> fits_to_csv mercury_line "[filename|directory]"
or using the windows executable:
>>> fits_to_csv.exe mercury_line "[filename|directory]"

mercury_line is a required argument, and expects an interger value between 300 and 400,
for the pixel x-value at which the 5461 Å line appears in the images to be converted.

If the second argument is not specified, the script will attempt to extract data from all
fits files in the current working directory. If a directory is specified, it extracts the data
from all fits files in that directory, creating the csv files in the same directory.
If a filename is specified, it only exctracts data from that file, creating the csv in the
file's directory.

For example:
>>> fits_to_csv 337 "image.FIT"
or:
>>> fits_to_csv 337 "Astronomy\Spectrograph\Images"
or:
>>> fits_to_csv 337 "C:\School\Astronomy\Spectrograph\Images\image.FIT"
or:
>>> fits_to_csv 337
The last one extracts data from all FITS files in the current working directory.
A non-absolute path will append the current working directry to the start of the path.

For more advanced use cases, such as getting binned data, cropping to a
specific part of the image (the defualt crop is like the original software's,
pixel 55 to 65), or using the image data for other things than extraction of
spectral data, the python package stispectrograph can be used to build other
tools. Other current functionality is getting the csv file as a string,
or converting to nm before saving as csv.

==========TODOS===========
-> Create better documentation for the stispectrograph package.
-> Create a visualisation of the spectrum, like the original software.
-> Create additional scripts, or a more universal tool.
-> Create standalone executables for other platforms.
-> Write the README file in Markdown or reStructuredText.

=========LICENSE==========
This software is abailable under the MIT License.
The full license can be found in "LICENSE.txt"

=====ACKNOWLEDGEMENTS=====
This software uses Astropy, available under the following license:

Copyright (c) 2011-2020, Astropy Developers

All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

Neither the name of the Astropy Team nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
