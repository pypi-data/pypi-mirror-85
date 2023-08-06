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

"""contains EDFTomoScan, class to be used with HDF5 acquisition"""


__authors__ = ["H.Payno"]
__license__ = "MIT"
__date__ = "09/08/2018"


from ..scanbase import TomoScanBase, _FOV
import json
import io
import os
import h5py
import numpy
from silx.io.url import DataUrl
from silx.utils.enum import Enum as _Enum
from tomoscan.utils import docstring
from tomoscan.io import HDF5File
from silx.io.utils import get_data
from ..unitsystem import metricsystem
from .utils import get_compacted_dataslices
import typing
import logging

_logger = logging.getLogger(__name__)


class ImageKey(_Enum):
    ALIGNMENT = -1
    PROJECTION = 0
    FLAT_FIELD = 1
    DARK_FIELD = 2
    INVALID = 3


class HDF5TomoScan(TomoScanBase):
    """
    This is the implementation of a TomoBase class for an acquisition stored
    in a HDF5 file.

    For now several property of the acquisition is accessible thought a getter
    (like get_scan_range) and a property (scan_range).

    This is done to be compliant with TomoBase instantiation. But his will be
    replace progressively by properties at the 'TomoBase' level

    :param scan: scan directory or scan masterfile.h5
    :param Union[str, None] entry: name of the NXtomo entry to select. If given
                                   index is ignored.
    :param Union[int, None] index: of the NXtomo entry to select. Ignored if
                                   an entry is specified. For consistency
                                   entries are ordered alphabetically
    """

    _TYPE = "hdf5"

    _DICT_ENTRY_KEY = "entry"

    _PROJ_PATH = "instrument/detector/data"

    _SCAN_META_PATH = "scan_meta/technique/scan"

    _DET_META_PATH = "scan_meta/technique/detector"

    _ROTATION_ANGLE_PATH = "sample/rotation_angle"

    _IMG_KEY_PATH = "instrument/detector/image_key"

    _IMG_KEY_CONTROL_PATH = "instrument/detector/image_key_control"

    _X_PIXEL_SIZE_PATH = "instrument/detector/x_pixel_size"

    _Y_PIXEL_SIZE_PATH = "instrument/detector/y_pixel_size"

    _X_PIXEL_MAG_SIZE_PATH = "instrument/detector/x_magnified_pixel_size"

    _Y_PIXEL_MAG_SIZE_PATH = "instrument/detector/y_magnified_pixel_size"

    _DISTANCE_PATH = "instrument/detector/distance"

    _FOV_PATH = "instrument/detector/field_of_view"

    _ESTIMATED_COR_FRM_MOTOR_PATH = "instrument/detector/estimated_cor_from_motor"

    _ENERGY_PATH = "beam/incident_energy"

    _SCHEME = "silx"

    _EPSILON_ROT_ANGLE = 0.02

    def __init__(
        self,
        scan: str,
        entry: str = None,
        index: typing.Union[int, None] = 0,
        ignore_projections: typing.Union[None, typing.Iterable] = None,
    ):
        if entry is not None:
            index = None
        # if the user give the master file instead of the scan dir...
        if scan is not None:
            if not os.path.exists(scan) and "." in os.path.split(scan)[-1]:
                self.master_file = scan
                scan = os.path.dirname(scan)
            elif os.path.isfile(scan) or ():
                self.master_file = scan
                scan = os.path.dirname(scan)
            else:
                self.master_file = self.get_master_file(scan)
        else:
            self.master_file = None

        super(HDF5TomoScan, self).__init__(
            scan=scan, type_=HDF5TomoScan._TYPE, ignore_projections=ignore_projections
        )

        if scan is None:
            self._entry = None
        else:
            self._entry = entry or self._get_entry_at(
                index=index, file_path=self.master_file
            )
            if self._entry is None:
                raise ValueError(
                    "unable to find a valid entry for %s" % self.master_file
                )
        # for now the default entry is 1_tomo but should change with time

        # data caches
        self._projections_compacted = None
        self._flats = None
        self._darks = None
        self._tomo_n = None
        # number of projections / radios
        self._dark_n = None
        # number of dark image made during acquisition
        self._ref_n = None
        # number of flat field made during acquisition
        self._scan_range = None
        # scan range, in degree
        self._dim_1, self._dim_2 = None, None
        # image dimensions
        self._x_pixel_size = None
        self._y_pixel_size = None
        self._x_magnified_pixel_size = None
        self._y_magnified_pixel_size = None
        # pixel dimensions (tuple)
        self._frames = None
        self._image_keys = None
        self._image_keys_control = None
        self._rotation_angles = None
        self._distance = None
        self._fov = None
        self._energy = None
        self._estimated_cor_frm_motor = None

    @staticmethod
    def get_master_file(scan_path):
        if os.path.isfile(scan_path):
            master_file = scan_path
        else:
            master_file = os.path.join(scan_path, os.path.basename(scan_path))
            if os.path.exists(master_file + ".nx"):
                master_file = master_file + ".nx"
            elif os.path.exists(master_file + ".hdf5"):
                master_file = master_file + ".hdf5"
            elif os.path.exists(master_file + ".h5"):
                master_file = master_file + ".h5"
            else:
                master_file = master_file + ".nx"
        return master_file

    @docstring(TomoScanBase.clear_caches)
    def clear_caches(self) -> None:
        super().clear_caches()
        self._projections = None
        self._projections_compacted = None
        self._flats = None
        self._darks = None
        self._tomo_n = None
        self._dark_n = None
        self._ref_n = None
        self._scan_range = None
        self._dim_1, self._dim_2 = None, None
        self._x_pixel_size = None
        self._y_pixel_size = None
        self._x_magnified_pixel_size = None
        self._y_magnified_pixel_size = None
        self._rotation_angles = None
        self._distance = None
        self._fov = None
        self._image_keys_control = None

    @staticmethod
    def _get_entry_at(index: int, file_path: str) -> str:
        """

        :param index:
        :param file_path:
        :return:
        """
        entries = HDF5TomoScan.get_valid_entries(file_path)
        if len(entries) == 0:
            return None
        else:
            return entries[index]

    @staticmethod
    def get_valid_entries(file_path: str) -> tuple:
        """
        return the list of 'Nxtomo' entries at the root level

        :param str file_path:
        :return: list of valid Nxtomo node (ordered alphabetically)
        :rtype: tuple

        ..note: entries are sorted to insure consistency
        """
        res = []
        res_buf = []

        if not os.path.isfile(file_path):
            raise ValueError("given file path should be a file")

        with HDF5File(file_path, "r", swmr=True) as h5f:
            for root_node in h5f.keys():
                node = h5f[root_node]
                if HDF5TomoScan.node_is_nxtomo(node) is True:
                    res_buf.append(root_node)  # cannnot be node because of sym links

            [res.append(node) for node in res_buf]
        res.sort()
        return tuple(res)

    @staticmethod
    def node_is_nxtomo(node: h5py.Group) -> bool:
        """check if the given h5py node is an nxtomo node or not"""
        if "NX_class" in node.attrs or "NXclass" in node.attrs:
            _logger.info(node.name + " is recognized as an nx class.")
        else:
            _logger.info(node.name + " is node an nx class.")
            return False
        if "definition" in node.attrs and node.attrs["definition"].lower() == "nxtomo":
            _logger.info(node.name + " is recognized as an NXtomo class.")
            return True
        else:
            return False

    @docstring(TomoScanBase.is_tomoscan_dir)
    @staticmethod
    def is_tomoscan_dir(directory: str, **kwargs) -> bool:
        if os.path.isfile(directory):
            master_file = directory
        else:
            master_file = HDF5TomoScan.get_master_file(scan_path=directory)
        if master_file:
            entries = HDF5TomoScan.get_valid_entries(file_path=master_file)
            return len(entries) > 0

    @docstring(TomoScanBase.is_abort)
    def is_abort(self, **kwargs):
        # for now there is no abort definition in .hdf5
        return False

    @docstring(TomoScanBase.to_dict)
    def to_dict(self) -> dict:
        res = super().to_dict()
        res[self.DICT_PATH_KEY] = self.master_file
        res[self._DICT_ENTRY_KEY] = self.entry
        return res

    @staticmethod
    def from_dict(_dict: dict):
        scan = HDF5TomoScan(scan=None)
        scan.load_from_dict(_dict=_dict)
        return scan

    @docstring(TomoScanBase.load_from_dict)
    def load_from_dict(self, _dict: dict) -> TomoScanBase:
        """

        :param _dict:
        :return:
        """
        if isinstance(_dict, io.TextIOWrapper):
            data = json.load(_dict)
        else:
            data = _dict
        if not (self.DICT_TYPE_KEY in data and data[self.DICT_TYPE_KEY] == self._TYPE):
            raise ValueError("Description is not an HDF5Scan json description")
        if HDF5TomoScan._DICT_ENTRY_KEY not in data:
            raise ValueError("No hdf5 entry specified")

        assert self.DICT_PATH_KEY in data
        self._entry = data[self._DICT_ENTRY_KEY]
        self.master_file = self.get_master_file(data[self.DICT_PATH_KEY])

        if os.path.isdir(data[self.DICT_PATH_KEY]):
            self.path = data[self.DICT_PATH_KEY]
        else:
            self.path = os.path.dirname(data[self.DICT_PATH_KEY])
        return self

    @property
    def entry(self) -> str:
        return self._entry

    @property
    @docstring(TomoScanBase.projections)
    def projections(self) -> typing.Union[dict, None]:
        if self._projections is None:
            if self.frames:
                ignored_projs = []
                if self.ignore_projections is not None:
                    ignored_projs = self.ignore_projections
                proj_frames = tuple(
                    filter(
                        lambda x: (
                            x.image_key == ImageKey.PROJECTION
                            and x.index not in ignored_projs
                            and x.is_control == False
                        ),
                        self.frames,
                    )
                )
                self._projections = {}
                for proj_frame in proj_frames:
                    self._projections[proj_frame.index] = proj_frame.url
        return self._projections

    @projections.setter
    def projections(self, projections: dict):
        self._projections = projections

    @property
    @docstring(TomoScanBase.alignment_projections)
    def alignment_projections(self) -> typing.Union[dict, None]:
        if self._alignment_projections is None:
            if self.frames:
                proj_frames = tuple(
                    filter(
                        lambda x: x.image_key == ImageKey.PROJECTION
                        and x.is_control == True,
                        self.frames,
                    )
                )
                self._alignment_projections = {}
                for proj_frame in proj_frames:
                    self._alignment_projections[proj_frame.index] = proj_frame.url
        return self._alignment_projections

    @property
    @docstring(TomoScanBase.darks)
    def darks(self) -> typing.Union[dict, None]:
        if self._darks is None:
            if self.frames:
                dark_frames = tuple(
                    filter(lambda x: x.image_key == ImageKey.DARK_FIELD, self.frames)
                )
                self._darks = {}
                for dark_frame in dark_frames:
                    self._darks[dark_frame.index] = dark_frame.url
        return self._darks

    @property
    @docstring(TomoScanBase.flats)
    def flats(self) -> typing.Union[dict, None]:
        if self._flats is None:
            if self.frames:
                flat_frames = tuple(
                    filter(lambda x: x.image_key == ImageKey.FLAT_FIELD, self.frames)
                )
                self._flats = {}
                for flat_frame in flat_frames:
                    self._flats[flat_frame.index] = flat_frame.url
        return self._flats

    @docstring(TomoScanBase.update)
    def update(self) -> None:
        """update list of radio and reconstruction by parsing the scan folder"""
        if self.master_file is None or not os.path.exists(self.master_file):
            return
        self.projections = self._get_projections_url()
        # TODO: update darks and flats too

    @docstring(TomoScanBase.get_proj_angle_url)
    def _get_projections_url(self):
        if self.master_file is None or not os.path.exists(self.master_file):
            return
        frames = self.frames
        if frames is not None:
            urls = {}
            for frame in frames:
                if frame.image_key is ImageKey.PROJECTION:
                    urls[frame.index] = frame.url
            return urls
        else:
            return None

    @docstring(TomoScanBase.tomo_n)
    @property
    def tomo_n(self) -> typing.Union[None, int]:
        """we are making two asumptions for computing tomo_n:
        - if a rotation = scan_range +/- EPSILON this is a return projection
        - The delta between each projections is constant
        """
        if (
            self._tomo_n is None
            and self.master_file
            and os.path.exists(self.master_file)
        ):
            if self.projections:
                return len(self.projections)
            else:
                return None
        else:
            return None

    @property
    def return_projs(self) -> typing.Union[None, list]:
        """"""
        frames = self.frames
        if frames:
            return_frames = list(filter(lambda x: x.is_control == True, frames))
            return return_frames
        else:
            return None

    @property
    def rotation_angle(self) -> typing.Union[None, list]:
        if self._rotation_angles is None:
            self._check_hdf5scan_validity()
            with HDF5File(self.master_file, "r", swmr=True) as h5_file:
                _rotation_angles = h5_file[self._entry][self._ROTATION_ANGLE_PATH][()]
                # cast in float
                self._rotation_angles = tuple(
                    [float(angle) for angle in _rotation_angles]
                )
        return self._rotation_angles

    @property
    def image_key(self) -> typing.Union[list, None]:
        if self._entry and self._image_keys is None:
            self._check_hdf5scan_validity()
            with HDF5File(self.master_file, "r", swmr=True) as h5_file:
                self._image_keys = h5_file[self._entry][self._IMG_KEY_PATH][()]
        return self._image_keys

    @property
    def image_key_control(self) -> typing.Union[list, None]:
        if self._entry and self._image_keys_control is None:
            self._check_hdf5scan_validity()
            with HDF5File(self.master_file, "r", swmr=True) as h5_file:
                if self._IMG_KEY_CONTROL_PATH in h5_file[self._entry]:
                    self._image_keys_control = h5_file[self._entry][
                        self._IMG_KEY_CONTROL_PATH
                    ][()]
                else:
                    self._image_keys_control = None
        return self._image_keys_control

    @docstring(TomoScanBase.dark_n)
    @property
    def dark_n(self) -> typing.Union[None, int]:
        if self.darks is not None:
            return len(self.darks)
        else:
            return None

    @docstring(TomoScanBase.ref_n)
    @property
    def ref_n(self) -> typing.Union[None, int]:
        if self.flats is not None:
            return len(self.flats)
        else:
            return None

    @docstring(TomoScanBase.ff_interval)
    @property
    def ff_interval(self):
        raise NotImplementedError(
            "not implemented for hdf5. But we have " "acquisition sequence instead."
        )

    @docstring(TomoScanBase.scan_range)
    @property
    def scan_range(self) -> typing.Union[None, int]:
        """For now scan range should return 180 or 360. We don't expect other value."""
        if (
            self._scan_range is None
            and self.master_file
            and os.path.exists(self.master_file)
            and self._entry is not None
        ):
            rotation_angle = self.rotation_angle
            if rotation_angle is not None:
                dist_to180 = abs(180 - numpy.max(rotation_angle))
                dist_to360 = abs(360 - numpy.max(rotation_angle))
                if dist_to180 < dist_to360:
                    self._scan_range = 180
                else:
                    self._scan_range = 360
        return self._scan_range

    @property
    def dim_1(self) -> typing.Union[None, int]:
        if self._dim_1 is None:
            self._get_dim1_dim2()
        return self._dim_1

    @property
    def dim_2(self) -> typing.Union[None, int]:
        if self._dim_2 is None:
            self._get_dim1_dim2()
        return self._dim_2

    @property
    def pixel_size(self) -> typing.Union[None, float]:
        """return x pixel size in meter"""
        return self.x_pixel_size

    @property
    def x_pixel_size(self) -> typing.Union[None, float]:
        """return x pixel size in meter"""
        if (
            self._x_pixel_size is None
            and self.master_file
            and os.path.exists(self.master_file)
        ):
            self._x_pixel_size, self._y_pixel_size = self._get_x_y_pixel_values()

        return self._x_pixel_size

    def _get_x_y_pixel_values(self):
        """read x and y pixel values"""
        with HDF5File(self.master_file, "r", swmr=True) as h5_file:
            x_pixel_dataset = h5_file[self._entry][self._X_PIXEL_SIZE_PATH]
            _x_pixel_size = self._get_value(x_pixel_dataset, default_unit="meter")
            y_pixel_dataset = h5_file[self._entry][self._Y_PIXEL_SIZE_PATH]
            _y_pixel_size = self._get_value(y_pixel_dataset, default_unit="meter")
        return _x_pixel_size, _y_pixel_size

    def _get_x_y_magnified_pixel_values(self):
        with HDF5File(self.master_file, "r", swmr=True) as h5_file:
            x_m_pixel_dataset = h5_file[self._entry][self._X_PIXEL_MAG_SIZE_PATH]
            _x_m_pixel_size = self._get_value(x_m_pixel_dataset, default_unit="meter")
            y_m_pixel_dataset = h5_file[self._entry][self._Y_PIXEL_MAG_SIZE_PATH]
            _y_m_pixel_size = self._get_value(y_m_pixel_dataset, default_unit="meter")
        return _x_m_pixel_size, _y_m_pixel_size

    def _get_fov(self):
        with HDF5File(self.master_file, "r", swmr=True, libver="latest") as h5_file:
            if self._FOV_PATH in h5_file[self._entry]:
                fov = h5_file[self._entry][self._FOV_PATH][()]
                return _FOV.from_value(fov)
            else:
                return None

    def _get_estimated_cor_frm_motor(self):
        with HDF5File(self.master_file, "r", swmr=True, libver="latest") as h5_file:
            if self._ESTIMATED_COR_FRM_MOTOR_PATH in h5_file[self._entry]:
                value = h5_file[self._entry][self._ESTIMATED_COR_FRM_MOTOR_PATH][()]
                return float(value)
            else:
                return None

    def _get_dim1_dim2(self):
        if self.master_file and os.path.exists(self.master_file):
            if self.projections is not None:
                if len(self.projections) > 0:
                    self._dim_2, self._dim_1 = get_data(
                        list(self.projections.values())[0]
                    ).shape

    @property
    def y_pixel_size(self) -> typing.Union[None, float]:
        """return y pixel size in meter"""
        if (
            self._y_pixel_size is None
            and self.master_file
            and os.path.exists(self.master_file)
        ):
            self._x_pixel_size, self._y_pixel_size = self._get_x_y_pixel_values()
        return self._y_pixel_size

    @property
    def x_magnified_pixel_size(self) -> typing.Union[None, float]:
        """return x magnified pixel size in meter"""
        if (
            self._x_magnified_pixel_size is None
            and self.master_file
            and os.path.exists(self.master_file)
        ):
            (
                self._x_magnified_pixel_size,
                self._y_magnified_pixel_size,
            ) = self._get_x_y_magnified_pixel_values()
        return self._x_magnified_pixel_size

    @property
    def y_magnified_pixel_size(self) -> typing.Union[None, float]:
        """return y magnified pixel size in meter"""
        if (
            self._y_magnified_pixel_size is None
            and self.master_file
            and os.path.exists(self.master_file)
        ):
            (
                self._x_magnified_pixel_size,
                self._y_magnified_pixel_size,
            ) = self._get_x_y_magnified_pixel_values()
        return self._y_magnified_pixel_size

    @property
    def distance(self) -> typing.Union[None, float]:
        """return sample detector distance in meter"""
        if (
            self._distance is None
            and self.master_file
            and os.path.exists(self.master_file)
        ):
            self._check_hdf5scan_validity()
            with HDF5File(self.master_file, "r", swmr=True) as h5_file:
                distance_dataset = h5_file[self._entry][self._DISTANCE_PATH]
                self._distance = self._get_value(distance_dataset, default_unit="m")
        return self._distance

    @property
    @docstring(TomoScanBase.field_of_view)
    def field_of_view(self):
        if self._fov is None and self.master_file and os.path.exists(self.master_file):
            self._fov = self._get_fov()
        return self._fov

    @property
    @docstring(TomoScanBase.estimated_cor_frm_motor)
    def estimated_cor_frm_motor(self):
        if (
            self._estimated_cor_frm_motor is None
            and self.master_file
            and os.path.exists(self.master_file)
        ):
            self._estimated_cor_frm_motor = self._get_estimated_cor_frm_motor()
        return self._estimated_cor_frm_motor

    @property
    def energy(self) -> typing.Union[None, float]:
        """energy in keV"""
        if (
            self._energy is None
            and self.master_file
            and os.path.exists(self.master_file)
        ):
            self._check_hdf5scan_validity()
            with HDF5File(self.master_file, "r", swmr=True) as h5_file:
                energy_dataset = h5_file[self._entry][self._ENERGY_PATH]
                self._energy = self._get_value(energy_dataset, default_unit="keV")
        return self._energy

    @property
    def frames(self) -> typing.Union[None, tuple]:
        """return tuple of frames. Frames contains """
        if self._frames is None:
            image_keys = self.image_key
            rotation_angles = self.rotation_angle
            if len(image_keys) != len(rotation_angles):
                raise ValueError(
                    "`rotation_angle` and `image_key` have "
                    "incoherent size (%s vs %s). Unable to "
                    "deduce frame properties" % (len(rotation_angles), len(image_keys))
                )
            self._frames = []

            def is_return(
                lframe, llast_proj_frame, ldelta_angle, return_already_reach
            ) -> tuple:
                """return is_return, delta_angle"""
                if ImageKey.from_value(img_key) is not ImageKey.PROJECTION:
                    return False, None
                if ldelta_angle is None and llast_proj_frame is not None:
                    delta_angle = (
                        lframe.rotation_angle - llast_proj_frame.rotation_angle
                    )
                    return False, delta_angle
                elif return_already_reach:
                    return True, ldelta_angle
                else:
                    current_angle = (
                        lframe.rotation_angle - llast_proj_frame.rotation_angle
                    )
                    return abs(current_angle) <= 2 * ldelta_angle, ldelta_angle

            delta_angle = None
            last_proj_frame = None
            return_already_reach = False
            for i_frame, rot_a, img_key in zip(
                range(len(rotation_angles)), rotation_angles, image_keys
            ):
                url = DataUrl(
                    file_path=self.master_file,
                    data_slice=(i_frame),
                    data_path=self.entry + "/instrument/detector/data",
                    scheme="silx",
                )

                frame = Frame(
                    index=i_frame, url=url, image_key=img_key, rotation_angle=rot_a
                )
                if self.image_key_control is not None:
                    is_control_frame = (
                        self.image_key_control[frame.index] == ImageKey.ALIGNMENT.value
                    )
                else:
                    return_already_reach, delta_angle = is_return(
                        lframe=frame,
                        llast_proj_frame=last_proj_frame,
                        ldelta_angle=delta_angle,
                        return_already_reach=return_already_reach,
                    )
                    is_control_frame = return_already_reach
                frame._is_control_frame = is_control_frame
                self._frames.append(frame)
                last_proj_frame = frame
            self._frames = tuple(self._frames)
        return self._frames

    @docstring(TomoScanBase.get_proj_angle_url)
    def get_proj_angle_url(self) -> typing.Union[dict, None]:
        if self.frames is not None:
            res = {}
            for frame in self.frames:
                if frame.image_key is ImageKey.PROJECTION:
                    if frame.is_control is False:
                        res[frame.rotation_angle] = frame.url
                    else:
                        res[str(frame.rotation_angle) + "(1)"] = frame.url
            return res
        else:
            return None

    @property
    def projections_compacted(self):
        """
        Return a compacted view of projection frames.

        :return: Dictionary where the key is a list of indices, and the value
            is the corresponding `silx.io.url.DataUrl` with merged data_slice
        :rtype: dict
        """
        if self._projections_compacted is None:
            self._projections_compacted = get_compacted_dataslices(self.projections)
        return self._projections_compacted

    def __str__(self):
        return "hdf5 scan(path: %s, master_file: %s, entry: %s)" % (
            self.path,
            self.master_file,
            self.entry,
        )

    @staticmethod
    def _get_value(node: h5py.Group, default_unit: str):
        """convert the value contained in the node to the adapted unit.
        Unit can be defined in on of the group attributes. It it is the case
        will pick this unit, otherwise will use the default unit
        """
        value = node[()]
        if "unit" in node.attrs:
            unit = node.attrs["unit"]
        elif "units" in node.attrs:
            unit = node.attrs["units"]
        else:
            unit = default_unit
        return value * metricsystem.MetricSystem.from_value(unit).value

    def _check_hdf5scan_validity(self):
        if self.master_file is None:
            raise ValueError("No master file provided")
        if self.entry is None:
            raise ValueError("No entry provided")
        with HDF5File(self.master_file, "r", swmr=True) as h5_file:
            if self._entry not in h5_file:
                raise ValueError(
                    "Given entry %s is not in the master "
                    "file %s" % (self._entry, self.master_file)
                )


class Frame:
    """class to store all metadata information of a frame"""

    def __init__(
        self,
        index: int,
        url: typing.Union[None, DataUrl] = None,
        image_key: typing.Union[None, ImageKey, int] = None,
        rotation_angle: typing.Union[None, float] = None,
        is_control_proj: bool = False,
    ):
        assert type(index) is int
        self._index = index
        self._image_key = ImageKey.from_value(image_key)
        self._rotation_angle = rotation_angle
        self._url = url
        self._is_control_frame = is_control_proj
        self._data = None

    @property
    def index(self) -> int:
        return self._index

    @property
    def image_key(self) -> ImageKey:
        return self._image_key

    @image_key.setter
    def image_key(self, image_key: ImageKey) -> None:
        self._image_key = image_key

    @property
    def rotation_angle(self) -> float:
        return self._rotation_angle

    @rotation_angle.setter
    def rotation_angle(self, angle: float) -> None:
        self._rotation_angle = angle

    @property
    def url(self) -> DataUrl:
        return self._url

    @property
    def is_control(self) -> bool:
        return self._is_control_frame

    @is_control.setter
    def is_control(self, is_return: bool):
        self._is_control_frame = is_return

    def __str__(self):
        return (
            "Frame {index},: image_key: {image_key},"
            "is_control: {is_control},"
            "rotation_angle: {rotation_angle},"
            "url: {url}".format(
                index=self.index,
                image_key=self.image_key,
                is_control=self.is_control,
                rotation_angle=self.rotation_angle,
                url=self.url.path(),
            )
        )
