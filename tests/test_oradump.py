import unittest
import tempfile
import os
from dotenv import load_dotenv
from datetime import datetime as dt
from pathlib import Path
from oradump import oradump

ENV_FILE = Path.cwd().parent / '.env'
TEMPLATES_PATH = Path.cwd() / 'templates'
TNS_PATH = Path.cwd() / 'tns'

class OraDumpAsrUralskTests(unittest.TestCase):
    def setUp(self):
        load_dotenv(ENV_FILE)
        self.source_code = "asr_uralsk"
        with open(TNS_PATH / self.source_code) as f:
            tns = f.read()
        self.sqlplus_conn_str = "{}/{}@{}".format(os.getenv("ASR_USER"), os.getenv("ASR_PASS"), tns)
        self.csv_dir = Path(tempfile.gettempdir()) / 'oradump'
        self.csv_dir.mkdir(parents=True, exist_ok=True)

    def test_asr_uralsk_tdr_for_first_five_days_of_feb(self):
        def date_for_csv(d):
            return dt.strptime(d, oradump.DATE_FORMAT).strftime("%Y%m%d")
        params = {"dtbegin": "01.02.2018", "dtend": "05.02.2018"}
        csv = self.csv_dir / "{}_{}-{}.csv".format("asr_uralsk", date_for_csv(params["dtbegin"]), date_for_csv(params["dtend"]))
        template_path = Path(TEMPLATES_PATH / 'db.tdr.sqtmpl')
        session = oradump.OraDump(self.source_code, self.sqlplus_conn_str)
        row_count = session.dump(template_path.read_text(encoding="utf8"), csv, params)
        self.assertIsInstance(row_count, int)
        self.assertGreater(row_count, 0)
