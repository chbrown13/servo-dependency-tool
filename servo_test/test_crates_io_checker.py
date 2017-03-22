import unittest
import os
import sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0,path)
import crates_io_checker as crates
from cargo_lock_parser import LockPackage

class TestCratesIOChecker(unittest.TestCase):

	def setUp(self):
		self.package = LockPackage()
		self.package.name = "test"
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

	def test_check_upgrade(self):
		self.assertFalse(crates.check_upgrade(self.package))
		self.assertTrue(crates.check_upgrade(self.package1))
		self.assertFalse(crates.check_upgrade(self.package2))

