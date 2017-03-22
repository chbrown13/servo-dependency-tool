import unittest
import os
import sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0,path)
import cargo_lock_parser as parser
from cargo_lock_parser import LockRoot, LockDependency, LockPackage, LockFile

class TestCargoLockParser(unittest.TestCase):

	def setUp(self):
		self.path = os.path.join(path,"test")

		self.root = LockRoot()
		self.root.name = "webvr_traits"
		self.root.version = "0.0.1"

		self.depend1 = LockDependency()
		self.depend1.name = "ipc-channel"
		self.depend1.version = "0.7.0"
		self.depend1.source = "(registry+https://github.com/rust-lang/crates.io-index)"

		self.package = LockPackage()
		self.package.name = "servo"
		self.package.version = "0.0.1"
		self.package.source = ""

		self.depend2 = LockDependency()
		self.depend2.name = "android_injected_glue"
		self.depend2.version = "0.2.1"
		self.depend2.source = "(git+https://github.com/mmatyas/android-rs-injected-glue)"

	def test_lock_file_parse(self):
		file = parser.lock_file_parse("Cargo.lock")
		self.assertEqual(type(file),LockFile)
		
		root = file.root
		self.assertEqual(root.name,self.root.name)
		self.assertEqual(root.version,self.root.version)
		self.assertEqual(len(root.dependencies),5)

		self.assertEqual(root.dependencies[0].name,self.depend1.name)
		self.assertEqual(root.dependencies[0].version,self.depend1.version)
		self.assertEqual(root.dependencies[0].source,self.depend1.source)

		self.assertEqual(len(file.packages),319)
		pkg = file.packages["servo"]
		self.assertEqual(pkg.name,self.package.name)
		self.assertEqual(pkg.version,self.package.version)
		self.assertEqual(pkg.source,self.package.source)
		self.assertFalse(pkg.upgrade_available)

		self.assertEqual(len(pkg.dependencies),18)
		dpd = pkg.dependencies[0]
		self.assertEqual(dpd.name,self.depend2.name)
		self.assertEqual(dpd.version,self.depend2.version)
		self.assertEqual(dpd.source,self.depend2.source)



