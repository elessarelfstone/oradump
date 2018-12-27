import attr
from datetime import datetime

def date_converter(s):
    return datetime.strptime(s, '%d.%m.%Y')

@attr.s
class SystemContext:
    source_code = attr.ib()
    conn_str = attr.ib()
    tmp_dir = attr.ib()
    uuid = attr.ib()
    main_template_path = attr.ib()
    script_template_path = attr.ib()
    csv_output_file = attr.ib()
    crc_output_file = attr.ib()

    @classmethod
    def from_tuple(cls, tpl):
        return cls(*tpl)

@attr.s
class Params:
    table = attr.ib()
    dtbegin = attr.ib(converter=date_converter)
    dtend = attr.ib(converter=date_converter)
    dtsys = attr.ib(converter=date_converter)

    @classmethod
    def from_tuple(cls, tpl):
        return cls(*tpl)

    @classmethod
    def asdict(cls, params):
        res = dict()
        res['table'] = params.table
        res['dtbegin'] = datetime.strftime(params.dtbegin, "%d.%m.%Y")
        res['dtend'] = datetime.strftime(params.dtend, "%d.%m.%Y")
        res['dtsys'] = datetime.strftime(params.dtsys, "%d.%m.%Y")
        return res





