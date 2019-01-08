import re
from pathlib import Path
from subprocess import Popen, PIPE
from datetime import datetime
import attr
from utils import Utils


def is_datetime(instance, attribute, value):
    try:
        dt = datetime.strptime(value, '%d.%m.%Y')
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


class OraDump:
    main_template = "main.sqtmpl"

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

    def _prepare_script(self, template, csv, params):
        crc = csv.parent / "{}.crc".format(csv.stem)
        script = self.main_template.format(csv, template.format(params), crc)
        return script

    def _run_script(self, script):
        session = Popen(["sqlplus", "-S", self.conn_str], stdout=PIPE, stdin=PIPE, stderr=PIPE)
        session.stdin.write(script.encode())
        out, err = session.communicate('\n exit;'.encode())
        return session.returncode, err, out

    def dump(self, template, csv, params):
        try:
            csv.parents[0].mkdir(parents=True, exist_ok=True)
            script = self._prepare_script(template, csv, params)
            rcode, err, out = self._run_script(script)
            if rcode != 0:
                raise Exception(self._get_sqlplus_message(out))
            return Utils.file_row_count(csv)
        except Exception:
            raise



