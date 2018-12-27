import os
import sqlite3
import logging
from pathlib import Path
from datetime import datetime
import uuid
import settings
from exceptions import *
from ora_params import SystemContext, Params


class OraSystem:
    _csv_name_format = "{}_{}.csv"
    _crc_name_format = "{}_{}.crc"
    sql_template_suffix = "sqtmpl"
    main_template = "main.sqtmpl"
    # test
    login = "reporter"
    password = "ciuyrhvv"

    def __init__(self, code):
        self._code = code
        self._set_envs()
        self._set_logger()
        self._source = self._sources_data()

        self._conn_str = self._sqlplus_conn_str()
        self.sys_date = datetime.today()
        self._uuid = str(uuid.uuid4())

    def _set_envs(self):
        """
        Gets and sets env variables from .env file and make some paths if they are not exists
        """
        self._app_name = os.getenv("APP_NAME")
        self._tmp_dir = os.getenv("TMP_DIR")
        self._logs_dir = os.getenv("LOGS_DIR")
        self._data_dir = os.getenv("DATA_DIR")
        self._sources = os.getenv("SOURCES_DB_FILE")
        self._work_dir = os.path.dirname(os.path.abspath(__file__))
        self._templates_dir = os.path.join(self._work_dir, 'templates')

        Path(self._tmp_dir).mkdir(parents=True, exist_ok=True)
        Path(self._logs_dir).mkdir(parents=True, exist_ok=True)
        Path(self._data_dir).mkdir(parents=True, exist_ok=True)

    def _set_logger(self):
        # logger settings
        """
        Makes a new logger and sets some settings for it
        """
        self._logger = logging.getLogger(self._app_name)
        self._logger.setLevel(logging.DEBUG)

        file_formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

        log_file = datetime.today().strftime('%Y%m') + '.log'
        file_handler = logging.FileHandler(Path(self._logs_dir) / log_file)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(file_formatter)

        console_formatter = logging.Formatter('%(asctime)s  %(message)s')

        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(console_formatter)

        self._logger.addHandler(console)
        self._logger.addHandler(file_handler)

    def _sources_data(self):
        """
        Gets detail info of all data sources from .db file(sqlite)
        :return: List of dicts for each data source in .db file
        """
        try:
            conn = sqlite3.connect('db/sources.db')
            c = conn.cursor()
            c.execute("SELECT * FROM data_sources WHERE code = '{}'".format(self._code))
            col_names = [desc[0] for desc in c.description]
            row = c.fetchone()
            result = {}
            for name, value in zip(col_names, row):
                result[name] = value
            return result
        except Exception as e:
            self._logger.error(e)

    def _sqlplus_conn_str(self):
        """
        Builds connections string for sqlplus(Oracle client)
        :return: {user}/{password}@{tns} formatted string
        """
        return "{}/{}@{}".format(self._source["user"], self._source["password"], self._source["conn_detail"])

    def get_logger(self):
        """
        Gets the logger of self
        :return:
        """
        return self._logger

    def get_scheme_and_table(self, table):
        pieces = table.split('.')
        self.asda = "asdasd"
        if len(pieces) == 2:
            return pieces
        else:
            return None

    def _period_as_str(self, dtbegin, dtend):
        """
        :return: string representation for period between dtbegin and dtend
        example: 01.01.2018-10.01.2018
        """
        return "{}-{}".format(dtbegin.strftime("%Y%m%d"), dtend.strftime("%Y%m%d"))

    def _template_path(self, table):
        """
        :return: script file path *.sqtmpl for specified table
        """
        file = "{}.{}".format(table, self.sql_template_suffix)
        template_path = Path(self._templates_dir) / file
        if not os.path.exists(template_path):
            raise ScriptPrepException("Template don't exists.", table)
        return template_path

    def _main_template_path(self):
        """
        :return: main_template file
        """
        return Path(self._templates_dir) / self.main_template

    def _csv_path_for_period(self, table, dtbegin: datetime, dtend: datetime, dtsys: datetime):
        """

        :param table: table that we're making csv file for
        :param dtbegin: start date for script
        :param dtend: last date for script
        :param dtsys:
        :return: csv file path for period
        """
        return Path(self._data_dir) / self._code / dtsys.strftime('%Y%m') / self._csv_name_format.format(table, self._period_as_str(dtbegin, dtend))

    def _crc_path_for_period(self, table, dtbegin:datetime, dtend:datetime, dtsys:datetime):
        """
        :param table: table that we're making crc file for
        :param dtbegin: start date for script
        :param dtend: last date for script
        :return: output crc file path for period
        """
        return Path(self._data_dir) / self._code / dtsys.strftime('%Y%m') / \
               self._crc_name_format.format(table, self._period_as_str(dtbegin, dtend))

    def _csv_path_for_day(self, table, dt):
        """
        :param table:
        :param dt:
        :return: get output csv file path for day
        """
        return self._csv_name_format.format(table, dt)

    def _crc_path_for_day(self, table, dt):
        """
        :param table:
        :param dt:
        :return: get output crc file path for day
        """
        return self._crc_name_format.format(table, dt)

    def get_context(self, params: Params):
        """
        Gets env variables, paths of out files and other system information for extracting data from Oracle
        :param params: parameters that passed with certain extraction
        :return: instance of SystemContext class
        """
        return SystemContext.from_tuple(
            (
                self._code,
                self._conn_str,
                self._tmp_dir,
                self._uuid,
                self._main_template_path(),
                self._template_path(params.table),
                self._csv_path_for_period(params.table, params.dtbegin, params.dtend, params.dtsys),
                self._crc_path_for_period(params.table, params.dtbegin, params.dtend, params.dtsys)
            )
        )





