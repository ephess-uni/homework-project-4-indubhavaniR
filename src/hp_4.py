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
    """
    Adds a daily date range to the list `values` beginning with
    `start_date`. The date, value pairs are returned as tuples
    in the returned list.

    Args:
        values (list): A daily sequence of numerical values.
        start_date (str): A date string with format yyyy-mm-dd representing the start date.

    Returns:
        list: A list of tuples where each tuple contains (date, value).
    """
    # Generate the date range starting from start_date
    date_objects = date_range(start_date, len(values))

    # Pair each date with the corresponding value
    date_value_pairs = list(zip(date_objects, values))
    return date_value_pairs

def fees_report(infile, outfile):
    """
    Calculates late fees per patron id and writes a summary report to outfile.

    Args:
        infile (str): The input CSV file containing book return information.
        outfile (str): The output CSV file to write the summary report.

    Returns:
        None
    """
    # Dictionary to store late fees per patron
    late_fees_per_patron = defaultdict(float)

    # Read the input CSV file
    with open(infile, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            date_returned = datetime.strptime(row['date_returned'], '%m/%d/%y')
            date_due = datetime.strptime(row['date_due'], '%m/%d/%Y')
            late_days = max(0, (date_returned - date_due).days)
            late_fee = late_days * 0.25
            patron_id = row['patron_id']
            late_fees_per_patron[patron_id] += late_fee

    # Write the summary report to the output CSV file
    with open(outfile, 'w', newline='') as csvfile:
        fieldnames = ['patron_id', 'late_fees']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for patron_id, late_fee in late_fees_per_patron.items():
            # Ensure late_fee is formatted as floating point with 2 decimal places
            writer.writerow({'patron_id': patron_id, 'late_fees': '{:.2f}'.format(late_fee)})


    # Write the summary report to the output CSV file
    with open(outfile, 'w', newline='') as csvfile:
        fieldnames = ['patron_id', 'late_fees']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for patron_id, late_fee in late_fees_per_patron.items():
            writer.writerow({'patron_id': patron_id, 'late_fees': '{:.2f}'.format(late_fee)})




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
