#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Methods for data file i/o.
"""

def to_csv(dictionary, filename=None, headers=None, nm=False):
    """
    Save spectral data as csv.

    Parameters
    ----------
    dictionary : dict
        The dictrionary containing spectral data.
        Get using Image.get_spectral_data()
    filename : str, optional
        The name of the file to save data to.
        If omitted, returns the csv file as a string.
    headers : iterable, optional
        The headers to put on top of the csv.
        Default is ("Wavelength", "Intensity")
    nm : bool, optional
        Whether to convert Ånström to nanometers. The default is False.

    Returns
    -------
    0 if saved to file.
    csv-formatted string if filename is omitted.

    """

    if nm:
        dictionary = dict([(key/10, val) for key, val in dictionary.items()])

    if headers:
        # Implement some check to make sure it's valid
        headers = list(headers)
    else:
        headers = ["Wavelength", "Intensity"]

    if filename:
        with open(filename + ".csv", "w") as file:
            file.write(f"{headers[0]},{headers[1]}\n")
            for key, value in dictionary.items():
                file.write(f"{key},{value}\n")
    else:
        out = ""
        out += f"{headers[0]},{headers[1]}\n"
        for key, value in dictionary.items():
            out += f"{key},{value}\n"
        return out
    return 0
