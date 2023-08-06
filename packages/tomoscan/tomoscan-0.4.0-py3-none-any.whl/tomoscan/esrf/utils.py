# coding: utf-8
# /*##########################################################################
# Copyright (C) 2016-2020 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#############################################################################*/


__authors__ = ["H.Payno"]
__license__ = "MIT"
__date__ = "10/10/2019"


import os
import fabio
from silx.io.url import DataUrl
from typing import Union
import numpy


def get_parameters_frm_par_or_info(file_: str) -> dict:
    """
    Create a dictionary from the file with the information name as keys and
    their values as values

    :param file_: path to the file to parse
    :type file_: str
    :raises: ValueError when fail to parse some line.
    """
    assert os.path.exists(file_) and os.path.isfile(file_)
    ddict = {}
    f = open(file_, "r")
    lines = f.readlines()
    for line in lines:
        if not "=" in line:
            continue
        l = line.replace(" ", "")
        l = l.rstrip("\n")
        # remove on the line comments
        if "#" in l:
            l = l.split("#")[0]
        if l == "":
            continue
        try:
            key, value = l.split("=")
        except ValueError as e:
            raise ValueError('fail to extract information from "%s"' % l)
        else:
            ddict[key.lower()] = value
    return ddict


def extract_urls_from_edf(
    file_: str, start_index: Union[None, int], n_frames: Union[int, None] = None
) -> dict:
    """
    return one DataUrl for each frame contain in the file_

    :param file_: path to the file to parse
    :type file_: str
    :param n_frames: Number of frames in each edf file (inferred if not told)
    :type n_frames: Union[int, None]
    :param start_index:
    :type start_index: Union[None,start_index]
    """
    res = {}
    index = 0 if start_index is None else start_index
    if n_frames is None:
        with fabio.open(file_) as fabio_file:
            n_frames = fabio_file.nframes
    for i_frame in range(n_frames):
        res[index] = DataUrl(
            scheme="fabio",
            file_path=file_,
            data_slice=[
                i_frame,
            ],
        )
        index += 1
    return res


def get_compacted_dataslices(urls):
    """
    Regroup urls to get the data more efficiently.
    Build a structure mapping files indices to information on
    how to load the data: `{indices_set: data_location}`
    where `data_location` contains contiguous indices.

    :param dict urls: Dictionary where the key is an integer and the value is
                      a silx `DataUrl`.

    :return: Dictionary where the key is a list of indices, and the value is
             the corresponding `silx.io.url.DataUrl` with merged data_slice
    :rtype: dict
    """

    def _convert_to_slice(idx):
        if numpy.isscalar(idx):
            return slice(idx, idx + 1)
        # otherwise, assume already slice object
        return idx

    def is_contiguous_slice(slice1, slice2):
        if numpy.isscalar(slice1):
            slice1 = slice(slice1, slice1 + 1)
        if numpy.isscalar(slice2):
            slice2 = slice(slice2, slice2 + 1)
        return slice2.start == slice1.stop

    def merge_slices(slice1, slice2):
        return slice(slice1.start, slice2.stop)

    sorted_files_indices = sorted(urls.keys())
    idx0 = sorted_files_indices[0]
    first_url = urls[idx0]

    merged_indices = [[idx0]]
    data_location = [
        [
            first_url.file_path(),
            first_url.data_path(),
            _convert_to_slice(first_url.data_slice()),
        ]
    ]
    pos = 0
    curr_fp, curr_dp, curr_slice = data_location[pos]
    for idx in sorted_files_indices[1:]:
        url = urls[idx]
        next_slice = _convert_to_slice(url.data_slice())
        if (
            (url.file_path() == curr_fp)
            and (url.data_path() == curr_dp)
            and is_contiguous_slice(curr_slice, next_slice)
        ):
            merged_indices[pos].append(idx)
            merged_slices = merge_slices(curr_slice, next_slice)
            data_location[pos][-1] = merged_slices
            curr_slice = merged_slices
        else:  # "jump"
            pos += 1
            merged_indices.append([idx])
            data_location.append(
                [url.file_path(), url.data_path(), _convert_to_slice(url.data_slice())]
            )
            curr_fp, curr_dp, curr_slice = data_location[pos]

    # Format result
    res = {}
    for ind, dl in zip(merged_indices, data_location):
        # res[tuple(ind)] = DataUrl(file_path=dl[0], data_path=dl[1], data_slice=dl[2])
        res.update(
            dict.fromkeys(
                ind, DataUrl(file_path=dl[0], data_path=dl[1], data_slice=dl[2])
            )
        )
    return res
