from datetime import datetime
import tempfile
import attr


def is_datetime(instance, attribute, value):
    try:
        dt = datetime.strptime(value, '%d.%m.%Y')
    except:
        raise TypeError("{} is not instance of datetime".format(value))


@attr.s
class SystemContext:
    source_code = attr.ib()
    conn_str = attr.ib()
    temp_dir = attr.ib()
    data_dir = attr.ib()

    @classmethod
    def from_tuple(cls, tpl):
        return cls(*tpl)

@attr.s
class OraSqlParams:
    dtbegin = attr.ib(validator=attr.validators.optional([is_datetime]))
    dtend = attr.ib(validator=attr.validators.optional([is_datetime]))


    @classmethod
    def from_tuple(cls, tpl):
        return cls(*tpl)

    # @classmethod
    # def asdict(cls, params):
    #     for


class OraDump:
    main_template = "main.sqtmpl"

    def __init__(self, source_code, conn_str):
        self.source_code = source_code
        self.conn_str = conn_str
        # self.temp_dir = tempfile.gettempdir()

    def _prepare_script(self, template, csv, params):
        crc = csv.parent / "{}.crc".format(csv.stem)
        script = self.main_template.format(csv, template.format(params), crc)
        return script

    def _run_script(self, script):
        pass

    # def dump(self, ):
    #
    #

ora_params = OraSqlParams.from_tuple((None, "11.08.2018"))


