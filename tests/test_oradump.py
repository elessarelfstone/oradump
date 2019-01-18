import unittest
import tempfile
import os
from dotenv import load_dotenv
from datetime import datetime as dt
from pathlib import Path
from oradump import oradump

ENV_FILE = Path.cwd().parent / '.env'
TEMPLATES_PATH = Path.cwd() / 'templates'
TNS_FILES_PATH = Path.cwd() / 'tns'


def date_for_csv(d):
    return dt.strptime(d, oradump.DATE_FORMAT).strftime("%Y%m%d")

class TestOraDumpAsrUralsk(unittest.TestCase):
    def setUp(self):
        # load .env file to get user and password of Oracle database
        load_dotenv(ENV_FILE)
        self.source_code = "asr_uralsk"
        # get tns string
        tns_path_file = TNS_FILES_PATH / self.source_code
        with open(str(tns_path_file)) as f:
            tns = f.read()

        # build connection string we usually pass to sqlplus
        self.sqlplus_conn_str = "{}/{}@{}".format(os.getenv("ASR_USER"), os.getenv("ASR_PASS"), tns)
        self.csv_dir = Path(tempfile.gettempdir()) / 'oradump'
        self.csv_dir.mkdir(parents=True, exist_ok=True)

    def test_asr_uralsk_tdr_for_first_five_days_of_feb(self):
        params = {"dtbegin": "01.02.2018", "dtend": "05.02.2018"}
        csv = self.csv_dir / "{}_{}-{}.csv".format(self.source_code, date_for_csv(params["dtbegin"]), date_for_csv(params["dtend"]))
        template_path = Path(TEMPLATES_PATH / 'db.tdr.sqtmpl')
        session = oradump.OraDump(self.sqlplus_conn_str)
        csv_row_count, crc_row_count = session.dump(template_path.read_text(encoding="utf8"), csv, params)
        self.assertIsInstance(csv_row_count, int)
        self.assertIsInstance(crc_row_count, int)
        self.assertGreater(csv_row_count, 0)
        self.assertGreater(crc_row_count, 0)
        self.assertEqual(csv_row_count, crc_row_count)


class TestOraDumpAsrAlmaty(unittest.TestCase):
    def setUp(self):
        # load .env file to get user and password of Oracle database
        load_dotenv(ENV_FILE)
        self.source_code = "asr_almaty"
        # get tns string
        tns_path_file = TNS_FILES_PATH / self.source_code
        with open(str(tns_path_file)) as f:
            tns = f.read()

        # build connection string we usually pass to sqlplus
        self.sqlplus_conn_str = "{}/{}@{}".format(os.getenv("ASR_USER"), os.getenv("ASR_PASS"), tns)
        self.csv_dir = Path(tempfile.gettempdir()) / 'oradump'
        self.csv_dir.mkdir(parents=True, exist_ok=True)

    def test_asr_almaty_tdr_for_first_five_days_of_feb(self):
        params = {"dtbegin": "01.02.2018", "dtend": "05.02.2018"}
        csv = self.csv_dir / "{}_{}-{}.csv".format(self.source_code, date_for_csv(params["dtbegin"]), date_for_csv(params["dtend"]))
        template_path = Path(TEMPLATES_PATH / 'db.tdr.sqtmpl')
        session = oradump.OraDump(self.sqlplus_conn_str)
        csv_row_count, crc_row_count = session.dump(template_path.read_text(encoding="utf8"), csv, params)
        self.assertIsInstance(csv_row_count, int)
        self.assertIsInstance(crc_row_count, int)
        self.assertGreater(csv_row_count, 0)
        self.assertGreater(crc_row_count, 0)
        self.assertEqual(csv_row_count, crc_row_count)