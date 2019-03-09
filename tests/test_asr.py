import unittest
import tempfile
import os
from dotenv import load_dotenv
from datetime import datetime as dt
from datetime import timedelta as td
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
        self.source_code = "asr_ura"
        self.params = {"rdt_id": "3", "server_id": "64"}
        # get tns string
        tns_path_file = TNS_FILES_PATH / self.source_code
        with open(str(tns_path_file)) as f:
            tns = f.read()

        # build connection string we usually pass to sqlplus
        self.sqlplus_conn_str = "{}/{}@{}".format(os.getenv("ASR_USER"), os.getenv("ASR_PASS"), tns)
        self.csv_dir = Path(tempfile.gettempdir()) / 'oradump'
        self.csv_dir.mkdir(parents=True, exist_ok=True)

    def test_tdr_for_firstday_of_curr_month(self):
        first_day = dt.today().replace(day=1).strftime("%d.%m.%Y")
        params = dict({"date": first_day}, **self.params)

        csv = os.path.join(self.csv_dir, "{}_{}_{}.csv".format(self.source_code, 'db.tdr', date_for_csv(params["date"])))
        # csv = self.csv_dir / "{}_{}.csv".format(self.source_code, date_for_csv(params["date"]))
        template_path = Path(TEMPLATES_PATH / 'asr_db.tdr.sqtmpl')
        csv_count_rows = oradump.OraDump.dump(self.sqlplus_conn_str, template_path.read_text(encoding="utf8"), csv, params)
        self.assertGreater(csv_count_rows, 0)

    def test_tdr_for_yesterday(self):
        yesterday = dt.today() - td(days=1)
        params = dict({"date": yesterday.strftime("%d.%m.%Y")}, **self.params)
        csv = os.path.join(self.csv_dir, "{}_{}_{}.csv".format(self.source_code, 'db.tdr', date_for_csv(params["date"])))
        # csv = self.csv_dir / "{}_{}_{}.csv".format(self.source_code, 'db.tdr', date_for_csv(params["date"]))
        template_path = Path(TEMPLATES_PATH / 'asr_db.tdr.sqtmpl')
        csv_count_rows = oradump.OraDump.dump(self.sqlplus_conn_str, template_path.read_text(encoding="utf8"), csv, params)
        self.assertGreater(csv_count_rows, 0)

    def test_tdr_for_yesterday_compress(self):
        yesterday = dt.today() - td(days=1)
        params = dict({"date": yesterday.strftime("%d.%m.%Y")}, **self.params)
        gziped_csv = os.path.join(self.csv_dir, "{}_{}_{}.csv.gzip".format(self.source_code, 'db.tdr', date_for_csv(params["date"])))
        # gziped_csv = self.csv_dir, "{}_{}_{}.csv.gzip".format(self.source_code, 'db.tdr', date_for_csv(params["date"]))
        # gziped_csv = self.csv_dir / "{}_{}_{}.csv.gzip".format(self.source_code, 'db.tdr', date_for_csv(params["date"]))
        template_path = Path(TEMPLATES_PATH / 'asr_db.tdr.sqtmpl')
        csv_count_rows = oradump.OraDump.dump_gziped(self.sqlplus_conn_str, template_path.read_text(encoding="utf8"), gziped_csv, params, True)
        self.assertGreater(csv_count_rows, 0)

class TestOraDumpAsrAlmaty(unittest.TestCase):
    def setUp(self):
        # load .env file to get user and password of Oracle database
        load_dotenv(ENV_FILE)
        self.source_code = "asr_alm"
        self.params = {"rdt_id": "6", "server_id": "90"}
        # get tns string
        tns_path_file = TNS_FILES_PATH / self.source_code
        with open(str(tns_path_file)) as f:
            tns = f.read()

        # build connection string we usually pass to sqlplus
        self.sqlplus_conn_str = "{}/{}@{}".format(os.getenv("ASR_USER"), os.getenv("ASR_PASS"), tns)
        self.csv_dir = Path(tempfile.gettempdir()) / 'oradump'
        self.csv_dir.mkdir(parents=True, exist_ok=True)

    def test_tdr_for_firstday_of_curr_month(self):
        first_day = dt.today().replace(day=1).strftime("%d.%m.%Y")
        params = dict({"date": first_day}, **self.params)
        csv = self.csv_dir / "{}_{}_{}.csv".format(self.source_code, 'db.tdr', date_for_csv(params["date"]))
        template_path = Path(TEMPLATES_PATH / 'asr_db.tdr.sqtmpl')
        csv_count_rows = oradump.OraDump.dump(self.sqlplus_conn_str, template_path.read_text(encoding="utf8"), csv, params)
        self.assertGreater(csv_count_rows, 0)

    def test_tdr_for_yesterday(self):
        yesterday = dt.today() - td(days=1)
        params = dict({"date": yesterday.strftime("%d.%m.%Y")}, **self.params)
        csv = self.csv_dir / "{}_{}_{}.csv".format(self.source_code, 'db.tdr', date_for_csv(params["date"]))
        template_path = Path(TEMPLATES_PATH / 'asr_db.tdr.sqtmpl')
        csv_count_rows = oradump.OraDump.dump(self.sqlplus_conn_str, template_path.read_text(encoding="utf8"), csv, params)
        self.assertGreater(csv_count_rows, 0)


class TestOraDumpAsrKaraganda(unittest.TestCase):
    def setUp(self):
        # load .env file to get user and password of Oracle database
        load_dotenv(ENV_FILE)
        self.source_code = "asr_kar"
        self.params = {"rdt_id": "6", "server_id": "90"}
        # get tns string
        tns_path_file = TNS_FILES_PATH / self.source_code
        with open(str(tns_path_file)) as f:
            tns = f.read()

        # build connection string we usually pass to sqlplus
        self.sqlplus_conn_str = "{}/{}@{}".format(os.getenv("ASR_USER"), os.getenv("ASR_PASS"), tns)
        self.csv_dir = Path(tempfile.gettempdir()) / 'oradump'
        self.csv_dir.mkdir(parents=True, exist_ok=True)

    def test_tdr_for_firstday_of_curr_month(self):
        first_day = dt.today().replace(day=1).strftime("%d.%m.%Y")
        params = dict({"date": first_day}, **self.params)
        csv = self.csv_dir / "{}_{}_{}.csv".format(self.source_code, 'db.tdr', date_for_csv(params["date"]))
        template_path = Path(TEMPLATES_PATH / 'asr_db.tdr.sqtmpl')
        # session = oradump.OraDump(self.sqlplus_conn_str)
        csv_count_rows = oradump.OraDump.dump(self.sqlplus_conn_str, template_path.read_text(encoding="utf8"), csv, params)
        self.assertGreater(csv_count_rows, 0)

    def test_tdr_for_yesterday(self):
        yesterday = dt.today() - td(days=1)
        params = dict({"date": yesterday.strftime("%d.%m.%Y")}, **self.params)
        csv = self.csv_dir / "{}_{}_{}.csv".format(self.source_code, 'db.tdr', date_for_csv(params["date"]))
        template_path = Path(TEMPLATES_PATH / 'asr_db.tdr.sqtmpl')
        csv_count_rows = oradump.OraDump.dump(self.sqlplus_conn_str, template_path.read_text(encoding="utf8"), csv, params)
        self.assertGreater(csv_count_rows, 0)

