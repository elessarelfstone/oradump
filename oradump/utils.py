import os
import sys
import gzip
import shutil
import subprocess


class Utils():
    @staticmethod
    def file_row_count(file):
        """
        File's rows counting. Uses wc util
        :param file: target file
        :return: count of rows in file
        """
        p = subprocess.Popen(['wc', '-l', str(file)], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        result, err = p.communicate()
        if p.returncode != 0:
            raise IOError(err)
        return int(result.strip().split()[0])

    @staticmethod
    def gzip(file):
        """
        Gzip file
        :param file: target
        :return: gziped new file's path
        """
        gzip_file = file + '.gzip'
        with open(file, 'rb') as f_in:
            with gzip.open(gzip_file, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        return gzip_file


