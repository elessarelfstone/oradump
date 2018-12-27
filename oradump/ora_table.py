from pathlib import Path
from subprocess import Popen, PIPE
from exceptions import *
from utils import Utils
from ora_params import SystemContext, Params


class OraTable:

    @staticmethod
    def prepare_script_for_sqlplus(context: SystemContext, params: Params, table_type="big"):
        """
        Make a new sql script(in) for sqlplus(Oracle client) according passed parameters
        :param context: env variables, paths of out files and other system information
        :param params: parameters that we passing into new script, like dates, etc
        :param table_type: flag that indicates how much of data it will be ... draft
        :return: путь до сформированного скрипта, путь до выходного csv файла, путь до файла crc
        :return: path of a new sql-script, path of csv data file that will be produced by new script,
        path of control count of rows file that will be produced by new script
        """
        # getting sqlplus headers and setting output csv filename in it
        try:
            script_body = context.script_template_path.read_text(encoding="utf8").format(**Params.asdict(params))
            script = context.main_template_path.read_text(encoding="utf8").\
                format(context.csv_output_file, script_body, context.crc_output_file)
            out_script_path = Path(context.tmp_dir) / '{}_{}.sql'.\
                format(context.uuid, context.script_template_path.stem)
            out_script_path.write_text(script, encoding="utf8")
            return out_script_path, context.csv_output_file, context.crc_output_file
        except Exception as e:
            raise ScriptPrepException(str(e), params.table)

    @staticmethod
    def save_table_data_by_sqlplus(conn_str, script_path):
        """
        Just executes earlier prepared sql-script by sqlplus(Oracle client)
        :param conn_str: formatted connection string that will be used by sqlplus, that includes user, password and tns
        :param script_path: path to a sql-script
        :return: код выполнения, stderr ошибка, stdout
        :return: status of execution(success or not), stderr, stdout
        """
        script = '@' + script_path.read_text(encoding="utf8")
        session = Popen(["sqlplus", "-S", conn_str], stdout=PIPE, stdin=PIPE, stderr=PIPE)
        session.stdin.write(script.encode())
        out, err = session.communicate('\n exit;'.encode())
        return session.returncode, err, out

    @staticmethod
    def dump_table_data(context: SystemContext, params: Params):
        """
        Extracts data from specified source and table
        :param context: env variables, paths of out files and other system information
        :param params: parameters that we passing into new script, like dates, etc
        :return: flag that indicate how it has done, csv file rows count, value from crc file
        """

        try:
            success = False
            context.csv_output_file.parents[0].mkdir(parents=True, exist_ok=True)
            script, csv, crc = OraTable.prepare_script_for_sqlplus(context, params)
            return_code, err, out = OraTable.save_table_data_by_sqlplus(context.conn_str, script)
            if return_code != 0:
                raise SqlPlusExecutionException(out, params.table)
            real_rows_count = Utils.file_row_count(csv)
            crc_rows_count = int(Path(crc).read_text().strip())
            if real_rows_count == crc_rows_count:
                success = True
                gzip_file = Utils.gzip(str(csv))
            else:
                raise RowsCountMismatch(params.table)
            return success, gzip_file, real_rows_count, crc_rows_count
        except Exception as e:
            raise
