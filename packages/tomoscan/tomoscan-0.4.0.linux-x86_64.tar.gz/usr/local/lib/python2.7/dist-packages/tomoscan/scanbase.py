# coding: utf-8
# /*##########################################################################
# Copyright (C) 2016- 2020 European Synchrotron Radiation Facility
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
"""This modules contains base class for TomoScanBase"""

__authors__ = ["H.Payno"]
__license__ = "MIT"
__date__ = "09/10/2019"


import os
import typing
import logging
import numpy
from typing import Union, Iterable
from collections import OrderedDict
from .unitsystem.metricsystem import MetricSystem
from silx.utils.enum import Enum as _Enum
from silx.io.url import DataUrl
from silx.io.utils import get_data
import silx.io.utils
from math import ceil
from .progress import Progress
from bisect import bisect_left

_logger = logging.getLogger(__name__)


class _FOV(_Enum):
    """Possible existing field of view"""

    FULL = "Full"
    HALF = "Half"


class TomoScanBase:
    """
    Base Class representing a scan.
    It is used to obtain core information regarding an aquisition like
    projections, dark and flat field...

    :param scan: path to the root folder containing the scan.
    :type scan: Union[str,None]
    """

    DICT_TYPE_KEY = "type"

    DICT_PATH_KEY = "path"

    _SCHEME = None
    """scheme to read data url for this type of acquisition"""

    def __init__(
        self,
        scan: Union[None, str],
        type_: str,
        ignore_projections: Union[None, Iterable] = None,
    ):
        self.path = scan
        self._type = type_
        self._normed_flats = None
        """darks normed. When set a dict is expected with index as the key
           and median or median of darks serie as value"""
        self._normed_darks = None
        """flats normed. When set a dict is expected with index as the key
           and median or median of darks serie as value"""
        self._notify_ffc_rsc_missing = True
        """Should we notify the user if ffc fails because cannot find dark or
        flat. Used to avoid several warnings. Only display one"""
        self._projections = None
        self._alignment_projections = None
        self._flats_weights = None
        """list flats indexes to use for flat field correction and associate
        weights"""
        self.ignore_projections = ignore_projections

    def clear_caches(self):
        """clear caches. Might be call if some data changed after
        first read of data or metadata"""
        self._notify_ffc_rsc_missing = True
        self._alignment_projections = None
        self._flats_weights = None

    @property
    def normed_darks(self):
        return self._normed_darks

    def set_normed_darks(self, darks):
        self._normed_darks = darks

    @property
    def normed_flats(self):
        return self._normed_flats

    def set_normed_flats(self, flats):
        self._normed_flats = flats

    @property
    def path(self) -> Union[None, str]:
        """

        :return: path of the scan root folder.
        :rtype: Union[str,None]
        """
        return self._path

    @path.setter
    def path(self, path: Union[str, None]) -> None:
        if path is None:
            self._path = path
        else:
            assert type(path) is str
            self._path = os.path.abspath(path)

    @property
    def type(self) -> str:
        """

        :return: type of the scanBase (can be 'edf' or 'hdf5' for now).
        :rtype: str
        """
        return self._type

    @staticmethod
    def is_tomoscan_dir(directory: str, **kwargs) -> bool:
        """
        Check if the given directory is holding an acquisition

        :param str directory:
        :return: does the given directory contains any acquisition
        :rtype: bool
        """
        raise NotImplementedError("Base class")

    def is_abort(self, **kwargs) -> bool:
        """

        :return: True if the acquisition has been abort
        :rtype: bool
        """
        raise NotImplementedError("Base class")

    @property
    def flats(self) -> Union[None, dict]:
        """list of flats files"""
        return self._flats

    @flats.setter
    def flats(self, flats: Union[None, dict]) -> None:
        self._flats = flats

    @property
    def darks(self) -> Union[None, dict]:
        """list of darks files"""
        return self._darks

    @darks.setter
    def darks(self, darks: Union[None, dict]) -> None:
        self._darks = darks

    @property
    def projections(self) -> Union[None, dict]:
        """if found dict of projections urls with index during acquisition as
        key"""
        return self._projections

    @projections.setter
    def projections(self, projections: dict) -> None:
        self._projections = projections

    @property
    def alignment_projections(self) -> Union[None, dict]:
        """
        dict of projections made for alignment with acquisition index as key
        None if not found
        """
        return self._alignment_projections

    @alignment_projections.setter
    def alignment_projections(self, alignment_projs):
        self._alignment_projections = alignment_projs

    @property
    def dark_n(self) -> Union[None, int]:
        raise NotImplementedError("Base class")

    @property
    def tomo_n(self) -> Union[None, int]:
        """number of projection WITHOUT the return projections"""
        raise NotImplementedError("Base class")

    @property
    def ref_n(self) -> Union[None, int]:
        raise NotImplementedError("Base class")

    @property
    def pixel_size(self) -> Union[None, float]:
        raise NotImplementedError("Base class")

    def get_pixel_size(self, unit="m") -> Union[None, float]:
        if self.pixel_size:
            return self.pixel_size / MetricSystem.from_value(unit).value
        else:
            return None

    @property
    def dim_1(self) -> Union[None, int]:
        raise NotImplementedError("Base class")

    @property
    def dim_2(self) -> Union[None, int]:
        raise NotImplementedError("Base class")

    @property
    def ff_interval(self) -> Union[None, int]:
        raise NotImplementedError("Base class")

    @property
    def scan_range(self) -> Union[None, int]:
        raise NotImplementedError("Base class")

    @property
    def energy(self) -> Union[None, float]:
        """

        :return: incident beam energy in keV
        """
        raise NotImplementedError("Base class")

    @property
    def distance(self) -> Union[None, float]:
        """

        :return: sample / detector distance in meter
        """
        raise NotImplementedError("Base class")

    @property
    def field_of_view(self):
        """

        :return: field of view of the scan. None if unknow else Full or Half
        """
        raise NotImplementedError("Base class")

    @property
    def estimated_cor_frm_motor(self):
        """

        :return: Estimated center of rotation estimated from motor position
        :rtype: Union[None, float]. If return value is in [-frame_width, +frame_width]
        """
        raise NotImplementedError("Base class")

    def get_distance(self, unit="m") -> Union[None, float]:
        """

        :param Union[MetricSystem, str] unit: unit requested for the distance
        :return: sample / detector distance with the requested unit
        """
        if self.distance:
            return self.distance / MetricSystem.from_value(unit).value
        else:
            return None

    def update(self) -> None:
        """Parse the root folder and files to update informations"""
        raise NotImplementedError("Base class")

    def to_dict(self) -> dict:
        """

        :return: convert the TomoScanBase object to a dictionary.
                 Used to serialize the object for example.
        :rtype: dict
        """
        res = dict()
        res[self.DICT_TYPE_KEY] = self.type
        res[self.DICT_PATH_KEY] = self.path
        return res

    def load_from_dict(self, _dict: dict):
        """
        Load properties contained in the dictionnary.

        :param _dict: dictionary to load
        :type _dict: dict
        :return: self
        :raises: ValueError if dict is invalid
        """
        raise NotImplementedError("Base class")

    def equal(self, other) -> bool:
        """

        :param :class:`.ScanBase` other: instance to compare with
        :return: True if instance are equivalent

        ..note:: we cannot use the __eq__ function because this object need to be
                 pickable
        """
        return (
            isinstance(other, self.__class__)
            or isinstance(self, other.__class__)
            and self.type == other.type
            and self.path == other.path
        )

    def get_proj_angle_url(self) -> dict:
        """
        return a dictionary of all the projection. key is the angle of the
        projection and value is the url.

        Keys are int for 'standard' projections and strings for return
        projections.

        :return dict: angles as keys, radios as value.
        """
        raise NotImplementedError("Base class")

    @staticmethod
    def map_urls_on_scan_range(urls, n_projection, scan_range) -> dict:
        """
        map given urls to an angle regarding scan_range and number of projection.
        We take the hypothesis that 'extra projection' are taken regarding the
        'id19' policy:

         * If the acquisition has a scan range of 360 then:

            * if 4 extra projection, the angles are (270, 180, 90, 0)

            * if 5 extra projection, the angles are (360, 270, 180, 90, 0)

         * If the acquisition has a scan range of 180 then:

            * if 2 extra projections: the angles are (90, 0)

            * if 3 extra projections: the angles are (180, 90, 0)

        ..warning:: each url should contain only one radio.

        :param urls: dict with all the urls. First url should be
                     the first radio acquire, last url should match the last
                     radio acquire.
        :type urls: dict
        :param n_projection: number of projection for the sample.
        :type n_projection: int
        :param scan_range: acquisition range (usually 180 or 360)
        :type scan_range: float
        :return: angle in degree as key and url as value
        :rtype: dict

        :raises: ValueError if the number of extra images found and scan_range
                 are incoherent
        """
        assert n_projection is not None
        ordered_url = OrderedDict(sorted(urls.items(), key=lambda x: x))

        res = {}
        # deal with the 'standard' acquisitions
        for proj_i in range(n_projection):
            url = list(ordered_url.values())[proj_i]
            if n_projection == 1:
                angle = 0.0
            else:
                angle = proj_i * scan_range / (n_projection - 1)
            if proj_i < len(urls):
                res[angle] = url

        if len(urls) > n_projection:
            # deal with extra images (used to check if the sampled as moved for
            # example)
            extraImgs = list(ordered_url.keys())[n_projection:]
            if len(extraImgs) in (4, 5):
                if scan_range < 360:
                    _logger.warning(
                        "incoherent data information to retrieve"
                        "scan extra images angle"
                    )
                elif len(extraImgs) == 4:
                    res["270(1)"] = ordered_url[extraImgs[0]]
                    res["180(1)"] = ordered_url[extraImgs[1]]
                    res["90(1)"] = ordered_url[extraImgs[2]]
                    res["0(1)"] = ordered_url[extraImgs[3]]
                else:
                    res["360(1)"] = ordered_url[extraImgs[0]]
                    res["270(1)"] = ordered_url[extraImgs[1]]
                    res["180(1)"] = ordered_url[extraImgs[2]]
                    res["90(1)"] = ordered_url[extraImgs[3]]
                    res["0(1)"] = ordered_url[extraImgs[4]]
            elif len(extraImgs) in (2, 3):
                if scan_range > 180:
                    _logger.warning(
                        "incoherent data information to retrieve"
                        "scan extra images angle"
                    )
                elif len(extraImgs) is 3:
                    res["180(1)"] = ordered_url[extraImgs[0]]
                    res["90(1)"] = ordered_url[extraImgs[1]]
                    res["0(1)"] = ordered_url[extraImgs[2]]
                else:
                    res["90(1)"] = ordered_url[extraImgs[0]]
                    res["0(1)"] = ordered_url[extraImgs[1]]
            elif len(extraImgs) == 1:
                res["0(1)"] = ordered_url[extraImgs[0]]
            else:
                raise ValueError(
                    "incoherent data information to retrieve scan" "extra images angle"
                )
        return res

    def get_sinogram(self, line, subsampling=1):
        """
        extract the sinogram from projections

        :param int line: which sinogram we want
        :param int subsampling: subsampling to apply. Allows to skip some io

        :return: computed sinogram from projections
        :rtype: numpy.array
        """
        if (
            self.tomo_n is not None and self.dim_2 is not None and line > self.dim_2
        ) or line < 0:
            raise ValueError("requested line {} is not in the scan".format(line))

        if self.projections is not None:
            dim1, dim2 = self.dim_1, self.dim_2
            y_dim = ceil(self.tomo_n / subsampling)
            sinogram = numpy.empty((y_dim, dim1))
            _logger.info(
                "compute sinogram for line {} of {} (subsampling: {})".format(
                    line, self.path, subsampling
                )
            )
            advancement = Progress(
                name="compute sinogram for {}, line={},"
                "sampling={}".format(os.path.basename(self.path), line, subsampling)
            )
            advancement.setMaxAdvancement(self.tomo_n)
            projections = self.projections
            o_keys = list(projections.keys())
            o_keys.sort()
            for i_proj, proj_key in enumerate(o_keys):
                if i_proj % subsampling == 0:
                    proj_url = projections[proj_key]
                    proj = silx.io.utils.get_data(proj_url)
                    proj = self.flat_field_correction(
                        projs=[proj], proj_indexes=[i_proj]
                    )[0]
                    sinogram[i_proj // subsampling] = proj[line]
                advancement.increaseAdvancement(1)
            return sinogram
        else:
            return None

    def _frame_flat_field_correction(
        self,
        data: typing.Union[numpy.ndarray, DataUrl],
        index_proj: typing.Union[int, None],
        dark,
        flat_weights: dict,
    ):
        """
        compute flat field correction for a provided data from is index
        one dark and two flats (require also indexes)
        """
        assert isinstance(data, (numpy.ndarray, DataUrl))
        if isinstance(data, DataUrl):
            data = get_data(data)
        can_process = True

        if flat_weights in (None, {}):
            if self._notify_ffc_rsc_missing:
                _logger.error("cannot make flat field correction, flat not found")
            can_process = False
        else:
            for flat_index, _ in flat_weights.items():
                if flat_index not in self.normed_flats:
                    _logger.error(
                        "flat {} has been removed, unable to apply flat field"
                        "".format(flat_index)
                    )
                    can_process = False
                elif (
                    self.normed_flats is not None
                    and self.normed_flats[flat_index].ndim != 2
                ):
                    _logger.error(
                        "cannot make flat field correction, flat should be of "
                        "dimension 2"
                    )
                    can_process = False

        if can_process is False:
            self._notify_ffc_rsc_missing = False
            return data

        if len(flat_weights) == 1:
            flat_value = self.normed_flats[list(flat_weights.keys())[0]]
        elif len(flat_weights) == 2:
            flat_keys = list(flat_weights.keys())
            flat_1 = flat_keys[0]
            flat_2 = flat_keys[1]

            flat_value = (
                self.normed_flats[flat_1] * flat_weights[flat_1]
                + self.normed_flats[flat_2] * flat_weights[flat_2]
            )
        else:
            raise ValueError(
                "no more than two flats are expected and"
                "at least one shuold be provided"
            )

        div = flat_value - dark
        div[div == 0] = 1
        return (data - dark) / div

    def flat_field_correction(
        self, projs: typing.Iterable, proj_indexes: typing.Iterable
    ):
        """Apply flat field correction on the given data

        :param Iterable projs: list of projection (numpy array) to apply correction
                              on
        :param Iterable data proj_indexes: list of indexes of the projection in
                                         the acquisition sequence. Values can
                                         be int or None. If None then the
                                         index take will be the one in the
                                         middle of the flats taken.
        :return: corrected data: list of numpy array
        :rtype: list
        """
        assert isinstance(projs, typing.Iterable)
        assert isinstance(proj_indexes, typing.Iterable)

        def has_missing_keys():
            if proj_indexes is None:
                return False
            for proj_index in proj_indexes:
                if proj_index not in self._flats_weights:
                    return False
            return True

        if self._flats_weights in (None, {}) or has_missing_keys():
            self._flats_weights = self._get_flats_weights()

        if self._flats_weights in (None, {}):
            _logger.error("Unable to compute flat weights")

        darks = self._normed_darks
        if darks is not None and len(darks) > 0:
            # take only one dark into account for now
            dark = list(darks.values())[0]
        else:
            dark = None

        if dark is None:
            if self._notify_ffc_rsc_missing:
                _logger.error("cannot make flat field correction, dark not found")
                return [
                    get_data(proj) if isinstance(proj, DataUrl) else proj
                    for proj in projs
                ]

        if dark is not None and dark.ndim != 2:
            _logger.error(
                "cannot make flat field correction, dark should be of " "dimension 2"
            )
            return [
                get_data(proj) if isinstance(proj, DataUrl) else proj for proj in projs
            ]

        return [
            self._frame_flat_field_correction(
                data=frame,
                dark=dark,
                index_proj=proj_i,
                flat_weights=self._flats_weights[proj_i]
                if proj_i in self._flats_weights
                else None,
            )
            for frame, proj_i in zip(projs, proj_indexes)
        ]

    def _get_flats_weights(self):
        """compute flats indexes to use and weights for each projection"""
        if self.normed_flats is None:
            return None
        flats_indexes = sorted(self.normed_flats.keys())

        def get_weights(proj_index):
            if proj_index in flats_indexes:
                return {proj_index: 1.0}
            pos = bisect_left(flats_indexes, proj_index)
            left_pos = flats_indexes[pos - 1]
            if pos == 0:
                return {flats_indexes[0]: 1.0}
            elif pos > len(flats_indexes) - 1:
                return {flats_indexes[-1]: 1.0}
            else:
                right_pos = flats_indexes[pos]
                delta = right_pos - left_pos
                return {
                    left_pos: 1 - (proj_index - left_pos) / delta,
                    right_pos: 1 - (right_pos - proj_index) / delta,
                }

        if self.normed_flats is None or len(self.normed_flats) == 0:
            return {}
        else:
            res = {}
            for proj_index in self.projections:
                res[proj_index] = get_weights(proj_index=proj_index)
            return res
