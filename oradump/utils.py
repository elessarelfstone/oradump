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

    @staticmethod
    def clean_csv(file):
        """
        Cleans file from "selected rows" statement in the end
        :param file: target file
        """
        with open(file, "r+", encoding="utf-8") as f:
            f.seek(0, os.SEEK_END)
            pos = f.tell() - 4
            while pos > 0 and f.read(1) != "\n":
                pos -= 1
                f.seek(pos, os.SEEK_SET)
            if pos > 0:
                f.seek(pos, os.SEEK_SET)
                f.truncate()
            f.close()

    @staticmethod
    def py_tail(file, n):
        """
        Read last n rows of file
        :param file: target file
        :param n: number of rows
        :return: last n rows of file
        """
        bufsize = 8192
        fsize = os.stat(file).st_size
        itr = 0
        res = ''
        with open(file) as f:
            if bufsize > fsize:
                bufsize = fsize - 1
            data = []
            while True:
                itr += 1
                f.seek(fsize - bufsize * itr)
                data.extend(f.readlines())
                if len(data) >= n or f.tell() == 0:
                    res = ''.join(data[-n:])
                    break
        return res
