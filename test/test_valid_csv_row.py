
from asgs_db import ASGS_DB
import csv
import os


def test_valid_csv_row():
    # init the object
    asgs_db = None

    try:
        # create the DB object
        asgs_db = ASGS_DB(None, 'asgs_dashboard', 'TEST INSTANCE')
    except Exception:
        pass

    # get the test data file
    file_name = os.path.join(os.path.dirname(__file__), 'stationProps.csv')

    # open a test data file
    with open(file_name, 'r') as f:
        # create the CSV reader
        reader = csv.reader(f)

        # get the header columns
        header: list = next(reader)  # Skip the header row.

        # init an error counter
        err_count: int = 0

        # loop through the rows this should fail
        for index, row in enumerate(reader):
            # check the row. if anything is missing just note the issue and continue
            no_cols_data_msg: str = asgs_db.valid_csv_row(header, row)

            if no_cols_data_msg:
                # print(f'Row {index+2} had errant column(s): {no_cols_data_msg}')
                err_count += 1
                continue

        # expecting a number of rows missing column data, 20 errors total
        assert len(no_cols_data_msg) != 0 and err_count == 20

        # reset the file point
        f.seek(0)

        # recreate the CSV reader
        reader = csv.reader(f)

        # get the header columns
        header: list = next(reader)  # Skip the header row.

        # init an error counter
        err_count: int = 0

        # loop through the rows this should fail
        for index, row in enumerate(reader):
            # check the row. if anything is missing just note the issue and continue
            no_cols_data_msg: str = asgs_db.valid_csv_row(header, row, [5])

            if no_cols_data_msg:
                # print(f'Row {index+2} had errant column(s): {no_cols_data_msg}')
                err_count += 1
                continue

        # expecting last row to have missing column data, 1 error total
        assert no_cols_data_msg and err_count == 1

        # reset the file point
        f.seek(0)

        # recreate the CSV reader
        reader = csv.reader(f)

        # get the header columns
        header: list = next(reader)  # Skip the header row.

        # init an error counter
        err_count: int = 0

        # loop through the rows this should fail
        for index, row in enumerate(reader):
            # check the row. if anything is missing just note the issue and continue
            no_cols_data_msg: str = asgs_db.valid_csv_row(header, row, [1, 2, 3, 4, 5, 6, 7])

            if no_cols_data_msg:
                # print(f'Row {index+2} had errant column(s): {no_cols_data_msg}')
                err_count += 1
                continue

        # everything is optional, no errors expected
        assert not no_cols_data_msg and err_count == 0
