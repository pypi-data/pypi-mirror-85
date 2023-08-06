import getpass
import logging
import os
import sqlite3
import uuid
from datetime import datetime

from rabbitmqbaselibrary.common.report import Report


class History(object):
    def __init__(self, hist_path: str, db_name: str) -> None:
        self.__hist_path = hist_path
        self.__conn = sqlite3.connect(db_name)
        self.__initialise()

    def save_report(self, report: Report, input_data: str, env: str) -> None:
        c = self.__conn.cursor()
        output_file = self.__history_file_name('output')
        input_file = self.__history_file_name('input')
        # noinspection SqlResolve
        c.execute('''INSERT INTO History(input_file, output_file, environment, timestamp, user) VALUES (?,?,?,?,?)''',
                  (self.__file_name(input_file), self.__file_name(output_file), env, datetime.now(), getpass.getuser()))
        logging.debug('history record added')
        with open(output_file, '+w') as f:
            f.write(report.report())
            logging.debug('output file written in history folder')
        with open(input_file, '+w') as f:
            f.write(input_data)
            logging.debug('input file written in history folder')
        self.__conn.commit()
        logging.info(
            'Record input:{} output:{} env:{} user:{} added to history db.'.format(self.__file_name(input_file),
                                                                                   self.__file_name(output_file), env,
                                                                                   getpass.getuser()))

    def __history_file_name(self, prefix: str) -> str:
        return os.path.join(self.__hist_path, '{}/{}.json'.format(prefix, str(uuid.uuid4())))

    @staticmethod
    def __file_name(abs_path: str) -> str:
        return os.path.basename(abs_path)

    def __initialise(self) -> None:
        c = self.__conn.cursor()
        # noinspection SqlNoDataSourceInspection
        c.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name=?''', ('History',))
        if c.fetchone() is None:
            # noinspection SqlNoDataSourceInspection
            c.execute(
                '''CREATE TABLE History (id INTEGER PRIMARY KEY,  input_file varchar(80) NOT NULL,
                 output_file varchar(80), environment varchar(20), timestamp DATETIME, user varchar(20))''')
            logging.info('history database initialised.')
