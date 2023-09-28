# hp_4.py
#
import csv
from collections import defaultdict
from datetime import datetime, timedelta

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


def calculate_late_fee(due_date, return_date):
    due_date = datetime.strptime(due_date, '%m/%d/%Y')
    return_date = datetime.strptime(return_date, '%m/%d/%y')
    days_late = max(0, (return_date - due_date).days)
    return round(days_late * 0.25, 2)


def fees_report(infile, outfile):
    # Dictionary to store late fees for each patron_id
    late_fees = defaultdict(float)

    # Read CSV file and calculate late fees
    with open(infile, 'r') as file:
        reader = csv.DictReader(file)
        late_fees = defaultdict(float, {
            row['patron_id']: late_fees[row['patron_id']] + calculate_late_fee(row['date_due'], row['date_returned'])
            for row in reader
        })

    # Write the summary report to the output file
    with open(outfile, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['patron_id', 'late_fees'])
        for patron_id, fee in late_fees.items():
            writer.writerow([patron_id, "{:.2f}".format(fee)])


# Example usage
fees_report('book_returns.csv', 'late_fees_summary.csv')

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
