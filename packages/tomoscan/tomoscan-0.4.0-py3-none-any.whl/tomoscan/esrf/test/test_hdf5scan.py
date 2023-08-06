# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
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
# ###########################################################################*/
"""Unit test for the scan defined at the hdf5 format"""

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "16/09/2019"

import unittest
import shutil
import os
import tempfile
from tomoscan.test.utils import UtilsTest
from tomoscan.esrf.hdf5scan import HDF5TomoScan, ImageKey, Frame
from tomoscan.unitsystem import metricsystem
from silx.io.utils import get_data
import numpy


class HDF5TestBaseClass(unittest.TestCase):
    """base class for hdf5 unit test"""

    def get_dataset(self, hdf5_dataset_name):
        dataset_file = os.path.join(self.test_dir, hdf5_dataset_name)
        o_dataset_file = UtilsTest.getH5Dataset(folderID=hdf5_dataset_name)
        shutil.copy(src=o_dataset_file, dst=dataset_file)
        return dataset_file

    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.test_dir)


class TestHDF5Scan(HDF5TestBaseClass):
    """Basic test for the hdf5 scan"""

    def setUp(self) -> None:
        super(TestHDF5Scan, self).setUp()
        self.dataset_file = self.get_dataset("frm_edftomomill_twoentries.nx")
        self.scan = HDF5TomoScan(scan=self.dataset_file)

    def testGeneral(self):
        """some general on the HDF5Scan """
        self.assertEqual(self.scan.master_file, self.dataset_file)
        self.assertEqual(self.scan.path, os.path.dirname(self.dataset_file))
        self.assertEqual(self.scan.type, "hdf5")
        self.assertEqual(self.scan.entry, "entry0000")
        self.assertEqual(len(self.scan.flats), 42)
        self.assertEqual(len(self.scan.darks), 1)
        self.assertEqual(len(self.scan.return_projs), 3)
        proj_angles = self.scan.get_proj_angle_url()
        self.assertEqual(len(proj_angles), 1500 + 3)
        self.assertTrue(90 in proj_angles)
        self.assertTrue(24.0 in proj_angles)
        self.assertTrue("90.0(1)" in proj_angles)
        self.assertTrue("180.0(1)" in proj_angles)
        self.assertTrue(179.88 not in proj_angles)

        url_1 = proj_angles[0]
        self.assertTrue(url_1.is_valid())
        self.assertTrue(url_1.is_absolute())
        self.assertEqual(url_1.scheme(), "silx")
        # check conversion to dict
        _dict = self.scan.to_dict()
        scan2 = HDF5TomoScan.from_dict(_dict)
        self.assertEqual(scan2.master_file, self.scan.master_file)
        self.assertEqual(scan2.entry, self.scan.entry)

    def testFrames(self):
        """Check the `frames` property which is massively used under the
        HDF5TomoScan class"""
        frames = self.scan.frames
        # check some projections
        proj_2 = frames[24]
        self.assertTrue(isinstance(proj_2, Frame))
        self.assertEqual(proj_2.index, 24)
        numpy.isclose(proj_2.rotation_angle, 0.24)
        self.assertFalse(proj_2.is_control)
        self.assertEqual(proj_2.url.file_path(), self.scan.master_file)
        self.assertEqual(proj_2.url.data_path(), "entry0000/instrument/detector/data")
        self.assertEqual(proj_2.url.data_slice(), 24)
        self.assertEqual(proj_2.image_key, ImageKey.PROJECTION)
        self.assertEqual(get_data(proj_2.url).shape, (20, 20))
        # check last two non-return projection
        for frame_index in (1520, 1542):
            with self.subTest(frame_index=frame_index):
                frame = frames[frame_index]
                self.assertTrue(frame.image_key, ImageKey.PROJECTION)
                self.assertFalse(frame.is_control)

        # check some darks
        dark_0 = frames[0]
        self.assertEqual(dark_0.index, 0)
        numpy.isclose(dark_0.rotation_angle, 0.0)
        self.assertFalse(dark_0.is_control)
        self.assertEqual(dark_0.url.file_path(), self.scan.master_file)
        self.assertEqual(dark_0.url.data_path(), "entry0000/instrument/detector/data")
        self.assertEqual(dark_0.url.data_slice(), 0)
        self.assertEqual(dark_0.image_key, ImageKey.DARK_FIELD)
        self.assertEqual(get_data(dark_0.url).shape, (20, 20))

        # check some refs
        ref_1 = frames[2]
        self.assertEqual(ref_1.index, 2)
        numpy.isclose(ref_1.rotation_angle, 0.0)
        self.assertFalse(ref_1.is_control)
        self.assertEqual(ref_1.url.file_path(), self.scan.master_file)
        self.assertEqual(ref_1.url.data_path(), "entry0000/instrument/detector/data")
        self.assertEqual(ref_1.url.data_slice(), 2)
        self.assertEqual(ref_1.image_key, ImageKey.FLAT_FIELD)
        self.assertEqual(get_data(ref_1.url).shape, (20, 20))

        # check some return projections
        r_proj_0 = frames[1543]
        self.assertTrue(isinstance(r_proj_0, Frame))
        self.assertEqual(r_proj_0.index, 1543)
        numpy.isclose(r_proj_0.rotation_angle, 180)
        self.assertTrue(r_proj_0.is_control)
        self.assertEqual(r_proj_0.url.file_path(), self.scan.master_file)
        self.assertEqual(r_proj_0.url.data_path(), "entry0000/instrument/detector/data")
        self.assertEqual(r_proj_0.url.data_slice(), 1543)
        self.assertEqual(r_proj_0.image_key, ImageKey.PROJECTION)
        self.assertEqual(get_data(r_proj_0.url).shape, (20, 20))

    def testProjections(self):
        """Make sure projections are valid"""
        projections = self.scan.projections
        self.assertEqual(len(self.scan.projections), 1500)
        url_0 = projections[list(projections.keys())[0]]
        self.assertEqual(url_0.file_path(), os.path.join(self.scan.master_file))
        self.assertEqual(url_0.data_slice(), 22)
        # should be 4 but angles are truely missleading: 179.88, 180.0, 90, 0.
        # in this case we are not using any information from image_key_control
        # and we wait deduce 'return mode' from angles.
        self.assertEqual(len(self.scan.alignment_projections), 3)

    def testDark(self):
        """Make sure darks are valid"""
        n_dark = 1
        self.assertEqual(self.scan.dark_n, n_dark)
        darks = self.scan.darks
        self.assertEqual(len(darks), 1)
        # TODO check accumulation time

    def testFlats(self):
        """Make sure flats are valid"""
        n_flats = 42
        flats = self.scan.flats
        self.assertEqual(len(flats), n_flats)
        self.assertEqual(self.scan.ref_n, n_flats)
        with self.assertRaises(NotImplementedError):
            self.scan.ff_interval

    def testDims(self):
        self.assertEqual(self.scan.dim_1, 20)
        self.assertEqual(self.scan.dim_2, 20)

    def testAxisUtils(self):
        self.assertEqual(self.scan.scan_range, 180)
        self.assertEqual(self.scan.tomo_n, 1500)

        radios_urls_evolution = self.scan.get_proj_angle_url()
        self.assertEqual(len(radios_urls_evolution), 1503)
        self.assertEqual(radios_urls_evolution[0].file_path(), self.scan.master_file)
        self.assertEqual(radios_urls_evolution[0].data_slice(), 22)
        self.assertEqual(
            radios_urls_evolution[0].data_path(), "entry0000/instrument/detector/data"
        )

    def testDarkRefUtils(self):
        self.assertEqual(self.scan.tomo_n, 1500)
        pixel_size = self.scan.pixel_size
        self.assertTrue(pixel_size is not None)
        self.assertTrue(
            numpy.isclose(
                self.scan.pixel_size, 0.05 * metricsystem.MetricSystem.MILLIMETER.value
            )
        )
        self.assertTrue(numpy.isclose(self.scan.get_pixel_size(unit="micrometer"), 50))
        self.assertTrue(
            numpy.isclose(
                self.scan.x_pixel_size,
                0.05 * metricsystem.MetricSystem.MILLIMETER.value,
            )
        )
        self.assertTrue(
            numpy.isclose(
                self.scan.y_pixel_size,
                0.05 * metricsystem.MetricSystem.MILLIMETER.value,
            )
        )

    def testNabuUtil(self):
        self.assertTrue(numpy.isclose(self.scan.distance, -19.9735))
        self.assertTrue(numpy.isclose(self.scan.get_distance(unit="cm"), -1997.35))

    def testCompactedProjs(self):
        projs_compacted = self.scan.projections_compacted
        self.assertTrue(projs_compacted.keys() == self.scan.projections.keys())
        for i in range(22, 1520 + 1):
            self.assertTrue(projs_compacted[i].data_slice() == slice(22, 1521, None))
        for i in range(1542, 1543):
            self.assertTrue(projs_compacted[i].data_slice() == slice(1542, 1543, None))


class TestFlatFieldCorrection(HDF5TestBaseClass):
    """Test the flat field correction"""

    def setUp(self) -> None:
        super(TestFlatFieldCorrection, self).setUp()
        self.dataset_file = self.get_dataset("frm_edftomomill_twoentries.nx")
        self.scan = HDF5TomoScan(scan=self.dataset_file)

    def testFlatAndDarksSet(self):
        self.scan.set_normed_flats(
            {
                21: numpy.random.random(20 * 20).reshape((20, 20)),
                1520: numpy.random.random(20 * 20).reshape((20, 20)),
            }
        )
        self.scan.set_normed_darks({0: numpy.random.random(20 * 20).reshape((20, 20))})

        projs = []
        proj_indexes = []
        for proj_index, proj in self.scan.projections.items():
            projs.append(proj)
            proj_indexes.append(proj_index)
        normed_proj = self.scan.flat_field_correction(
            projs=projs, proj_indexes=proj_indexes
        )
        self.assertEqual(len(normed_proj), len(self.scan.projections))
        raw_data = get_data(projs[50])
        self.assertFalse(numpy.array_equal(raw_data, normed_proj[50]))

    def testNoFlatOrDarkSet(self):
        projs = []
        proj_indexes = []
        for proj_index, proj in self.scan.projections.items():
            projs.append(proj)
            proj_indexes.append(proj_index)
        with self.assertLogs("tomoscan", level="ERROR"):
            normed_proj = self.scan.flat_field_correction(
                projs=projs, proj_indexes=proj_indexes
            )
        self.assertEqual(len(normed_proj), len(self.scan.projections))
        raw_data = get_data(projs[50])
        self.assertTrue(numpy.array_equal(raw_data, normed_proj[50]))


class TestGetSinogram(HDF5TestBaseClass):
    """Test the get_sinogram function"""

    def setUp(self) -> None:
        super(TestGetSinogram, self).setUp()
        self.dataset_file = self.get_dataset("frm_edftomomill_twoentries.nx")
        self.scan = HDF5TomoScan(scan=self.dataset_file)
        # set some random dark and flats
        self.scan.set_normed_flats(
            {
                21: numpy.random.random(20 * 20).reshape((20, 20)),
                1520: numpy.random.random(20 * 20).reshape((20, 20)),
            }
        )
        self.scan.set_normed_darks({0: numpy.random.random(20 * 20).reshape((20, 20))})

    def testGetSinogram1(self):
        sinogram = self.scan.get_sinogram(line=12, subsampling=1)
        self.assertEqual(sinogram.shape, (1500, 20))

    def testGetSinogram2(self):
        """Test if subsampling is negative"""
        with self.assertRaises(ValueError):
            self.scan.get_sinogram(line=0, subsampling=-1)

    def testGetSinogram3(self):
        sinogram = self.scan.get_sinogram(line=0, subsampling=3)
        self.assertEqual(sinogram.shape, (500, 20))

    def testGetSinogram4(self):
        """Test if line is not in the projection"""
        with self.assertRaises(ValueError):
            self.scan.get_sinogram(line=-1, subsampling=1)

    def testGetSinogram5(self):
        """Test if line is not in the projection"""
        with self.assertRaises(ValueError):
            self.scan.get_sinogram(line=25, subsampling=1)


class TestIgnoredProjections(HDF5TestBaseClass):
    """Test the ignore_projections parameter"""

    def setUp(self) -> None:
        super(TestIgnoredProjections, self).setUp()
        self.dataset_file = self.get_dataset("frm_edftomomill_oneentry.nx")
        self.ignored_projs = [387, 388, 389, 390, 391, 392, 393, 394, 395, 396]

    def testIgnoreProjections(self):
        self.scan = HDF5TomoScan(
            scan=self.dataset_file, ignore_projections=self.ignored_projs
        )
        self.scan._projections = None
        for idx in self.ignored_projs:
            self.assertFalse(
                idx in self.scan.projections,
                "Projection index %d is supposed to be ignored" % idx,
            )


def suite():
    test_suite = unittest.TestSuite()
    for ui in (
        TestHDF5Scan,
        TestFlatFieldCorrection,
        TestGetSinogram,
        TestIgnoredProjections,
    ):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
