"""Tests for the FixedHashMap data structure."""

import pytest


@pytest.fixture
def fhm():
	from datastructures import FixedHashMap
	return FixedHashMap()


def test_init(fhm):
	assert "{}" == str(fhm)


def test_add_item(fhm):
	fhm['0'] = 1
	assert str(fhm) == "{'0': 1}"


# class TestFixedHashMap(unittest.TestCase):
# 	def setUp(self):
# 		'''Setting up for the test'''
# 		test_name =  self.shortDescription()
# 		self.test_fhm = None
#
# 		if "error" in test_name.lower():
# 			self.test_fhm = FixedHashMap(5)
# 		else:
# 			self.test_fhm = FixedHashMap()
#
# 	def tearDown(self):
# 		'''Cleaning up after the test'''
# 		del self.test_fhm
#
#
# 	def test01_add_item(self):
# 		'''Add an item to the fhm'''
# 		self.test_fhm['0'] = 1
# 		self.assertEquals(str(self.test_fhm), '{\'0\': 1}')
#
# 	def test02_get_item(self):
# 		'''Get an item from the fhm'''
# 		self.test_fhm['0'] = 1
# 		self.assertEquals(self.test_fhm['0'], 1)
#
# 	def test03_add_multiple_items(self):
# 		'''Add multiple items to the fhm'''
# 		self.test_fhm['0'] = 1
# 		self.test_fhm['1'] = 2
# 		self.assertEquals(str(self.test_fhm), '{\'0\': 1, \'1\': 2}')
#
# 	def test04_remove_item(self):
# 		'''Add then remove items to fhm'''
# 		self.test_fhm['0'] = 1
# 		self.assertEquals(str(self.test_fhm), '{\'0\': 1}')
# 		del self.test_fhm['0']
# 		self.assertEquals(str(self.test_fhm), "{}")
#
# 	def test05_get_load(self):
# 		'''Get load (default size is 1000)'''
# 		self.test_fhm['0'] = 1
# 		self.assertEquals(self.test_fhm.load(), 0.001)
#
# 	def test06_get_keys(self):
# 		'''Get keys from the fhm'''
# 		self.test_fhm['0'] = 1
# 		self.test_fhm['1'] = 2
# 		self.assertEquals(self.test_fhm.keys(), ['0', '1'])
#
# 	def test07_get_non_existant_key(self):
# 		'''Check error: try to get non-existant key'''
# 		self.assertRaises(Exception, self.test_fhm.get, '0')
#
# 	def test08_delete_non_existant_key(self):
# 		'''Check error: try to remove non-existant key'''
# 		self.assertRaises(Exception, self.test_fhm.delete, '0')
#
# 	def test09_delete_non_existant_key(self):
# 		'''Check error: try toadd non string key'''
# 		self.assertRaises(Exception, self.test_fhm.set, 1, 2)
#
# 	def test10_add_more_than_size(self):
# 		'''Check error: try to add more than size of fhm'''
# 		for i in range(5):
# 			self.test_fhm[str(i)] = i+1
# 		self.assertRaises(Exception, self.test_fhm.set, '5', 6)


# if __name__ == '__main__':
# 	suite = unittest.TestLoader().loadTestsFromTestCase(TestFixedHashMap)
# 	unittest.TextTestRunner(verbosity=2).run(suite)
