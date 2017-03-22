import unittest
import os
import sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0,path)
import crates_io_checker as crates
from cargo_lock_parser import LockPackage

class TestCratesIOChecker(unittest.TestCase):

	def setUp(self):
		self.path = path + "/servo_test/"

		self.package = LockPackage()
		self.package.name = "unittest"
		self.package.version = "1.0"
		self.package.source = "src"

		self.package1 = LockPackage()
		self.package1.name = "servo"
		self.package1.version = "1.0"
		self.package.source = "test"

		self.package2 = LockPackage()
		self.package2.name = "servo"
		self.package2.version = "2.0"
		self.package.source = "test"

		crates.depend = {"servo":[{"name":"servo","vers":"1.0","deps":[]},{"name":"servo","vers":"2.0","deps":[]}]}
		crates.CRATES = "cargo_test"

	def test_check_upgrade(self):
		self.assertFalse(crates.check_upgrade(self.package))
		self.assertTrue(crates.check_upgrade(self.package1))
		self.assertFalse(crates.check_upgrade(self.package2))

	def test_read_file(self):
		self.assertIsNone(crates.read_file(None))
		self.assertFalse('testing' in crates.depend.keys())
		read = crates.check_folder("testing",os.path.join(self.path,crates.CRATES,"te","st"))
		self.assertIsNotNone(read)
		crates.read_file(read)
		self.assertTrue('testing' in crates.depend.keys())

	def test_check_folder(self):
		self.assertIsNone(crates.check_folder("test.txt",self.path))
		self.assertEqual(os.path.join(self.path,"test_crates_io_checker.py"),crates.check_folder("test_crates_io_checker.py",self.path))

	def test_check_package(self):
		test = LockPackage()
		test.name = "testing"
		self.assertIsNotNone(crates.check_package(test))
		self.assertIsNone(crates.check_package(self.package))

	def test_check(self):
		crates.check(self.package1)
		self.assertTrue(self.package1.upgrade_available)
		crates.check(self.package2)
		self.assertFalse(self.package2.upgrade_available)
