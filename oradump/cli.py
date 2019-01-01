from datetime import datetime
import click

from ora_system import OraSystem
from ora_table import OraTable
from ora_params import Params
from decorators import logging, benchmark, exception


@click.command()
@click.option('--sourcecode')
@click.option('--table')
@click.option('--dtbegin')
@click.option('--dtend')
@click.option('--dtsys', default=datetime.today().strftime("%d.%m.%Y"))
def cli(sourcecode, table, dtbegin, dtend, dtsys):
    _sys = OraSystem(sourcecode)
    _from_cli = (table, dtbegin, dtend, dtsys)

    @benchmark(_sys.get_logger())
    @logging(Params.from_tuple(_from_cli).table, _sys.get_context(Params.from_tuple(_from_cli)).source_code, _sys.get_logger())
    @exception(_sys.get_logger())
    def run_dump(_sys, params):
        return OraTable.dump_table_data(_sys.get_context(Params.from_tuple(params)), Params.from_tuple(params))

    run_dump(_sys, _from_cli)


if __name__ == "__main__":
    cli()
