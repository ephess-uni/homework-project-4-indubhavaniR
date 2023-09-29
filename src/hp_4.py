# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


MONTHS = {
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr',
    5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug',
    9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
}


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
        element to a format dd mmm yyyy--01 Jan 2001."""
    reformatted_dates = []
    for date_str in old_dates:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        formatted_date = f"{date_obj.day:02d} {MONTHS[date_obj.month]} {date_obj.year}"
        reformatted_dates.append(formatted_date)
    return reformatted_dates


def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str):
        raise TypeError('start should be a string in yyyy-mm-dd format')
    if not isinstance(n, int):
        raise TypeError('n should be an integer')

    start_date = datetime.strptime(start, '%Y-%m-%d')
    date_objects = [start_date + timedelta(days=i) for i in range(n)]
    return date_objects


def add_date_range(values, start_date):
    date_objects = date_range(start_date, len(values))
    result = [(date_objects[i], values[i]) for i in range(len(values))]
    return result


def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""

    with open(infile) as file:
        added_list = []
        read_csv_obj = DictReader(file)
        for record in read_csv_obj:
            temp_dict = {}
            late_fee_days = datetime.strptime(record['date_returned'], '%m/%d/%Y') - datetime.strptime(
                record['date_due'], '%m/%d/%Y')
            if (late_fee_days.days > 0):
                temp_dict["patron_id"] = record['patron_id']
                temp_dict["late_fees"] = round(late_fee_days.days * 0.25, 2)
                added_list.append(temp_dict)
            else:
                temp_dict["patron_id"] = record['patron_id']
                temp_dict["late_fees"] = float(0)
                added_list.append(temp_dict)

        temp_dict_2 = {}
        for dict in added_list:
            key = (dict['patron_id'])
            temp_dict_2[key] = temp_dict_2.get(key, 0) + dict['late_fees']
        updated_list = [{'patron_id': key, 'late_fees': value} for key, value in temp_dict_2.items()]

        for dict in updated_list:
            for key, value in dict.items():
                if key == "late_fees":
                    if len(str(value).split('.')[-1]) != 2:
                        dict[key] = str(value) + "0"

    with open(outfile, "w", newline="") as file:
        col = ['patron_id', 'late_fees']
        writer = DictWriter(file, fieldnames=col)
        writer.writeheader()
        writer.writerows(updated_list)

# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':

    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
