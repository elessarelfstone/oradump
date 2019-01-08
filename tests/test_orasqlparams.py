import unittest
import oradump.oradump as oradump


class OraSqlParamsTests(unittest.TestCase):
	def test_date_format_from_tuple(self):
		test_tpl_params = ("10/09/2019", "10-09-2019")
		with self.assertRaises(TypeError):
			result = oradump.OraSqlParams.from_tuple(test_tpl_params)

	def test_date_format_from_dict(self):
		test_dict_params = dict(dtbegin="10-2019-14", dtend="10-2019-16")
		with self.assertRaises(TypeError):
			result = oradump.OraSqlParams.from_dict(test_dict_params)

