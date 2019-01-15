import re
from pathlib import Path
import os
from subprocess import Popen, PIPE
from datetime import datetime
import attr
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


@attr.s
class OraSqlParams:
    dtbegin = attr.ib(validator=attr.validators.optional([is_datetime]))
    dtend = attr.ib(validator=attr.validators.optional([is_datetime]))

    @classmethod
    def from_tuple(cls, tpl):
        return cls(*tpl)

    @classmethod
    def from_dict(cls, dct):
        return cls(**dct)


class OraDumpError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "{}:{}".format(self.__class__, self.message)


class OraDump:
    def __init__(self, source_code, conn_str):
        self.source_code = source_code
        self.conn_str = conn_str

    @staticmethod
    def _get_sqlplus_message(stdout):
        search = re.search(r'.*ORA.*', stdout)
        if search:
            mess = search.group(0).strip()
        else:
            mess = 'UNKHOWN'
        return mess

    @staticmethod
    def prepare_script(template, csv, params):
        crc = csv.parent / "{}.crc".format(csv.stem)
        script = Path(MAIN_TEMPLATE).read_text(encoding="utf8").format(csv, template.format(**params), crc)
        return script, crc

    def _run_script(self, script):
        session = Popen(["sqlplus", "-S", self.conn_str], stdout=PIPE, stdin=PIPE, stderr=PIPE)
        session.stdin.write(script.encode())
        out, err = session.communicate('\n exit;'.encode())
        return session.returncode, err, out

    def dump(self, template, csv, params, compress=True):
        try:
            csv.parents[0].mkdir(parents=True, exist_ok=True)
            script, crc = OraDump.prepare_script(template, csv, params)
            rcode, err, out = self._run_script(script)
            if rcode != 0:
                raise OraDumpError(self._get_sqlplus_message(out))

            csv_rows_cnt = Utils.file_row_count(csv)
            crc_rows_cnt = int(Path(crc).read_text().strip())

            if compress:
                try:
                    Utils.gzip(str(csv))
                finally:
                    os.remove(csv)

            return csv_rows_cnt, crc_rows_cnt
        except Exception:
            raise



