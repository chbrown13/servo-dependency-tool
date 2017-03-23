import unittest
import os
import sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0,path)
import cargo_toml_updater as updater
from cargo_lock_parser import lock_file_parse

class TestCargoTOMLUpdater(unittest.TestCase):

	def setUp(self):
		self.lock_file = lock_file_parse("Cargo.lock")
		self.lock_file.packages["servo"].upgrade_available = True
		self.lock_file.packages["toml"].upgrade_available = True
		self.lock_file.packages["rustc-serialize"].upgrade_available = True

		with open("Cargo.toml",'r') as f:
			self.original = f.read()

	def test_toml_file_update(self):
		updater.toml_file_update("Cargo.toml",self.lock_file)
		with open("Cargo.toml",'r') as f:
			update = f.read()
		self.assertNotEqual(self.original,update)

	def tearDown(self):
		with open("Cargo.toml",'w') as f:
			f.write(self.original)
		
