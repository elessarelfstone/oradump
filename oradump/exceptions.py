import re

#TODO добавить имана классов в сообщение

class OraError(Exception):
    def __init__(self):
        super().__init__(self, self.message)


class OraSystemError(Exception):
    def __init__(self, message):
        self.message = 'System object initialization failed with follow message :' + message

    def __str__(self):
        return "{}:{}".format(self.__class__.__name__, self.message)


class ScriptPrepException(OraError):
    def __init__(self, message, table):
        self.message = 'Preparation procedure failed with follow exception '\
                       + "\"" + message + "\"" + ' for ' + table

    def __str__(self):
        return "{}:{}".format(self.__class__.__name__, self.message)


class SqlPlusExecutionException(OraError):
    def __init__(self, message, table):

        search = re.search(r'.*ORA.*', message.decode("utf-8"))
        if search:
            mess = search.group(0).strip()
        else:
            mess = 'UNKHOWN'
        self.message = "Extract procedure failed for " + table + " with sqlplus error: " + "\"" + mess + "\""
        # super().__init__(self, self.message)

    def __str__(self):
        return "{}:{}".format(self.__class__.__name__, self.message)


class RowsCountMismatch(OraError):
    def __init__(self, table):
        self.message = "Count of rows in data file and control sum mismatch for " + table + " table"
        # super().__init__(self, self.message)

    def __str__(self):
        return "{}:{}".format(self.__class__.__name__, self.message)