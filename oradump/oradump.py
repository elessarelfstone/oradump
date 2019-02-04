import re
from pathlib import Path
import os
from subprocess import Popen, PIPE
from datetime import datetime
from oradump.utils import Utils


DATE_FORMAT = "%d.%m.%Y"
MAIN_TEMPLATE = Path(__file__).parent / "main.sqtmpl"


def is_datetime(instance, attribute, value):
    try:
        dt = datetime.strptime(value, DATE_FORMAT)
    except Exception:
        raise TypeError("{} is not instance of datetime".format(value))


def is_int(instance, attribute, value):
    try:
        int_val = int(value)
    except Exception:
        raise TypeError("{} is not instance of int".format(value))


class OraDumpError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "{}:{}".format(self.__class__, self.message)


class OraDump:
    def __init__(self, conn_str):
        self.conn_str = conn_str

    @staticmethod
    def _get_sqlplus_message(stdout):
        search = re.search(r'.*ORA.*', stdout.decode('utf-8'))
        if search:
            mess = search.group(0).strip()
        else:
            mess = 'UNKHOWN'
        return mess

    @staticmethod
    def prepare_script(template, csv, params):
        script = Path(MAIN_TEMPLATE).read_text(encoding="utf8").format(csv, template.format(**params))
        return script

    def run_script(self, script):
        session = Popen(["sqlplus", "-S", self.conn_str], stdout=PIPE, stdin=PIPE, stderr=PIPE)
        session.stdin.write(script.encode())
        out, err = session.communicate('\n exit;'.encode())
        return session.returncode, err, out

    def dump(self, template, csv, params, compress=False):
        try:
            csv.parents[0].mkdir(parents=True, exist_ok=True)
            script = OraDump.prepare_script(template, csv, params)
            rcode, err, out = self.run_script(script)
            if rcode != 0:
                raise OraDumpError(self._get_sqlplus_message(out))

            rows_count = Utils.file_row_count(csv)
            if compress:
                try:
                    Utils.gzip(str(csv))
                finally:
                    os.remove(csv)
            return rows_count
        except Exception:
            raise
