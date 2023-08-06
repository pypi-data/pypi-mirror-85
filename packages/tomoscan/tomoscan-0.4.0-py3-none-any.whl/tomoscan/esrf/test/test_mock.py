# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2017 European Synchrotron Radiation Facility
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

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "21/08/2020"

import unittest
import os
import tempfile
from tomoscan.esrf.mock import MockHDF5, MockEDF
from tomoscan.esrf.hdf5scan import HDF5TomoScan
import shutil


class TestMockEDFScan(unittest.TestCase):
    """Test that mock scan are adapted to other unit test"""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.scan_id = os.path.join(self.tmpdir, "myscan")

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def testScanEvolution360(self):
        """Test get scan evolution from a mock scan with a 360 range and no
        extra radio"""
        scan = MockEDF.mockScan(
            scanID=self.scan_id,
            nRadio=5,
            nRecons=1,
            nPagRecons=1,
            dim=10,
            scan_range=360,
        )
        scan_dynamic = scan.get_proj_angle_url()
        self.assertEqual(len(scan_dynamic), 5)
        self.assertTrue(0 in scan_dynamic)
        self.assertEqual(
            scan_dynamic[0].file_path(),
            os.path.join(self.tmpdir, "myscan", "myscan_0000.edf"),
        )
        self.assertTrue(180 in scan_dynamic)
        self.assertEqual(
            scan_dynamic[180].file_path(),
            os.path.join(self.tmpdir, "myscan", "myscan_0002.edf"),
        )
        self.assertTrue(360 in scan_dynamic)
        self.assertEqual(
            scan_dynamic[360].file_path(),
            os.path.join(self.tmpdir, "myscan", "myscan_0004.edf"),
        )

    def testScanEvolution180(self):
        """Test get scan evolution from a mock scan with a 180 range and no
        extra radio"""
        scan = MockEDF.mockScan(
            scanID=self.scan_id,
            nRadio=8,
            nRecons=0,
            nPagRecons=0,
            dim=10,
            scan_range=180,
        )
        scan_dynamic = scan.get_proj_angle_url()
        self.assertEqual(len(scan_dynamic), 8)
        self.assertTrue(0 in scan_dynamic)
        self.assertEqual(
            scan_dynamic[0].file_path(),
            os.path.join(self.tmpdir, "myscan", "myscan_0000.edf"),
        )
        self.assertTrue(180 in scan_dynamic)
        self.assertEqual(
            scan_dynamic[180].file_path(),
            os.path.join(self.tmpdir, "myscan", "myscan_0007.edf"),
        )
        self.assertFalse(360 in scan_dynamic)

    def testScanEvolution360Extra4(self):
        """Test get scan evolution from a mock scan with a 360 range and 4
        extra radio"""
        scan = MockEDF.mockScan(
            scanID=self.scan_id,
            nRadio=21,
            nRecons=0,
            nPagRecons=0,
            dim=10,
            scan_range=360,
            n_extra_radio=4,
        )
        scan_dynamic = scan.get_proj_angle_url()
        self.assertEqual(len(scan_dynamic), 21 + 4)
        self.assertTrue(0 in scan_dynamic)
        self.assertEqual(
            scan_dynamic[0].file_path(),
            os.path.join(self.tmpdir, "myscan", "myscan_0000.edf"),
        )
        self.assertTrue(180 in scan_dynamic)
        self.assertEqual(
            scan_dynamic[180].file_path(),
            os.path.join(self.tmpdir, "myscan", "myscan_0010.edf"),
        )
        self.assertTrue(360 in scan_dynamic)
        self.assertEqual(
            scan_dynamic[360].file_path(),
            os.path.join(self.tmpdir, "myscan", "myscan_0020.edf"),
        )
        extra_angles = (0, 90, 180, 270)  # note: 0(1) is the last file acquire
        for iAngle, angle in enumerate(extra_angles):
            angle_id = str(angle) + "(1)"
            self.assertTrue(angle_id in scan_dynamic)
            file_name = os.path.join(
                self.tmpdir, "myscan", "myscan_%04d.edf" % (21 + 4 - 1 - iAngle)
            )
            self.assertEqual(scan_dynamic[angle_id].file_path(), file_name)

    def testScanEvolution180Extra2(self):
        """Test get scan evolution from a mock scan with a 360 range and 3
        extra radios"""
        scan = MockEDF.mockScan(
            scanID=self.scan_id,
            nRadio=4,
            nRecons=2,
            nPagRecons=2,
            dim=10,
            scan_range=180,
            n_extra_radio=2,
        )
        scan_dynamic = scan.get_proj_angle_url()
        self.assertEqual(len(scan_dynamic), 4 + 2)
        self.assertTrue(0 in scan_dynamic)
        self.assertEqual(
            scan_dynamic[0].file_path(),
            os.path.join(self.tmpdir, "myscan", "myscan_0000.edf"),
        )
        self.assertTrue(180 in scan_dynamic)
        self.assertEqual(
            scan_dynamic[180].file_path(),
            os.path.join(self.tmpdir, "myscan", "myscan_0003.edf"),
        )
        self.assertTrue(360 not in scan_dynamic)
        extra_angles = (0, 90)  # note: 0(1) is the last file acquire
        for iAngle, angle in enumerate(extra_angles):
            angle_id = str(angle) + "(1)"
            self.assertTrue(angle_id in scan_dynamic)
            file_name = os.path.join(
                self.tmpdir, "myscan", "myscan_%04d.edf" % (4 + 2 - 1 - iAngle)
            )
            self.assertEqual(scan_dynamic[angle_id].file_path(), file_name)


class TestMockHDF5(unittest.TestCase):
    """Test the MockHDF5 file"""

    def setUp(self) -> None:
        self.folder = tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.folder)

    def test_creation(self):
        mock = MockHDF5(scan_path=self.folder, n_proj=10, n_ini_proj=10)
        self.assertEqual(
            mock.scan_master_file,
            os.path.join(self.folder, os.path.basename(self.folder) + ".h5"),
        )
        tomoScan = HDF5TomoScan(mock.scan_path, entry=mock.scan_entry)
        self.assertEqual(len(HDF5TomoScan.get_valid_entries(mock.scan_master_file)), 1)
        tomoScan.update()
        self.assertEqual(tomoScan.scan_range, 360)
        self.assertEqual(len(tomoScan.projections), 10)

    def testSimpleMockCreationOneCall(self):
        """Test mock of an acquisition starting by one dark, then 10 ref,
        then 20 radios, then 10 'final' ref and 2 alignment radio"""
        mock = MockHDF5(
            scan_path=self.folder,
            n_proj=20,
            n_ini_proj=20,
            n_alignement_proj=2,
            create_ini_dark=True,
            create_ini_ref=True,
            create_final_ref=True,
            n_refs=10,
        )
        self.assertTrue(0 in mock.scan.darks.keys())
        self.assertTrue(1 in mock.scan.flats.keys())
        self.assertTrue(10 in mock.scan.flats.keys())


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestMockHDF5, TestMockEDFScan):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
