import csv

from datetime import date, timedelta
from pathlib import Path


DATA_DIR = Path(__file__).resolve().with_name('historical_data')


def calculate_3day_before_change(file_path):
    """
    Calculate `3day_before_change` for passed file
    and write it to this file as new column.
    """
    # List to store each row for csv file as dict
    company_data = []

    # Get data from csv file
    # fill new list with inner dicts of rows
    # and add additional field for `3day_before_change`
    with open(f'{file_path}', mode='r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            company_data.append({
                'Date': row['Date'],
                'Open': row['Open'],
                'High': row['High'],
                'Low': row['Low'],
                'Close': row['Close'],
                'Adj Close': row['Adj Close'],
                'Volume': row['Volume'],
                '3day_before_change': '-',
            })

    # Calculate 3day_before_change
    for i in range(len(company_data)-1, 0, -1):
        desired_day = date.fromisoformat(company_data[i]['Date']) - timedelta(days=3)
        for y in range(1, 4):
            # Check if that day in range are 3 day before of current row
            if (
                    desired_day
                    ==
                    date.fromisoformat(company_data[i - y]['Date'])
            ):
                # Calculate 3day_before_change
                before_change = (
                        float(company_data[i]['Close'])
                        /
                        float(company_data[i - y]['Close'])
                )
                company_data[i]['3day_before_change'] = str(before_change)

    # Write new data to company's cvs file
    with open(f'{file_path}', mode='w') as csv_file:

        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                'Date', 'Open', 'High', 'Low',
                'Close', 'Adj Close', 'Volume',
                '3day_before_change',
            ]
        )
        writer.writeheader()
        writer.writerows(company_data)


def calculate_all_files(dir_path):
    """
    Loop through all csv files in passed dir
    and execute `calculate_3day_before_change()`
    on each file.
    """
    for path in Path(dir_path).rglob('*.csv'):
        calculate_3day_before_change(path)


if __name__ == '__main__':
    print('come here')
    calculate_all_files(DATA_DIR)
