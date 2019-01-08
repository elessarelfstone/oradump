import unittest
import oradump


class OraDumpTests(unittest.TestCase):
	def test_asr_uralsk_for_first_five_days_of_month(self):
		session = oradump.OraDump("asr_uralsk", "tns")
