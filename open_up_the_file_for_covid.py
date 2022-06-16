"""
Name: The negative consequences of COVID-19 on NAICS categorized industries in Canada
Part: open_up_the_file_for_covid

Module Description
===============================
This module contains open up and store the data from the covid datasets and make
output for the rest of the project program.

Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for this project,
please email Paul.He@mail.utoronto.ca.

This file is Copyright (c) 2021 Paul He, Jiawei Yu and Xiling Zhao."""

import datetime
import csv


def final_covid_sum_up(name: str) -> dict[datetime.date, int]:
    """Final version of sum up all covid cases monthly in the given file"""
    daily_case = open_and_process_covid_data(name)
    return sum_up_all_the_case_for_month(daily_case)


def open_and_process_covid_data(file_name: str) -> dict[datetime: int]:
    """
    The helper function of final_covid_sum_up, return Canada covid data stored in a csv file with
    the given filename.

    The return value is a dictionary consisting of two elements:

    - The key is the date.
    - The value is int represent how many covid cases grows in the key date

    Preconditions:
      - filename refers to a valid csv file with headers
      - file has to be download by the given URL
    """
    with open(file_name) as file:
        reader = csv.reader(file)
        data_so_far = {}
        for row in reader:
            # only the get the Canada covid data
            if row[1] == 'Canada':
                time = convert_str_to_datetime(row[3])
                case = int(row[15])
                data_so_far[time] = case
    return data_so_far


def sum_up_all_the_case_for_month(days: dict[datetime.date, int]) -> dict[datetime.date, int]:
    """ Sum up all the increasing covid cases for the month that the given dictionary has.

    Return a dictionary which the key represent month  and the value represen the total cases grows
    in that month

    >>> a = {datetime.date(2020, 7, 19): 339, datetime.date(2020, 7, 20): 786,\
            datetime.date(2021, 12, 4): 3608}
    >>> sum_up_all_the_case_for_month(a)
    {datetime.date(2020, 7, 1): 1125, datetime.date(2021, 12, 1): 3608}
    """
    case_for_month = []
    final = {}
    possible_year = set()
    # get all possible year appear in the given days
    for day in days:
        possible_year.add(day.year)
    # add up all the cases for the month in the parameter days
    for year in possible_year:
        for month in range(1, 13):
            search_day(days, case_for_month, year, month)
    # add the month and the total case to the dictionary if the accumulator is not empty
            if case_for_month != []:
                final[datetime.date(year, month, 1)] = sum(case_for_month)
                case_for_month = []
    return final


def search_day(days: dict[datetime, int], accumulator: list, year: int, month: int) -> None:
    """The helper function of sum_up_all_the_case_for_month"""
    for day in days:
        if day.month == month and day.year == year:
            accumulator.append(days[day])


def convert_str_to_datetime(date: str) -> datetime:
    """Return a datetime based on the given date

    Preconditions:
        - len(date) == 10
        _ the given date has to be this format: 'yyyy-mm-dd'

    >>> convert_str_to_datetime('2002-09-16')
    datetime.date(2002, 9, 16)
    >>> convert_str_to_datetime('2003-03-15')
    datetime.date(2003, 3, 15)
    >>> convert_str_to_datetime('2003-01-07')
    datetime.date(2003, 1, 7)
    """
    date = str.split(date, '-')
    year = int(date[0])
    month = int(date[1])
    day = int(date[2])
    return datetime.date(year, month, day)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['csv', 'datetime'],
        'allowed-io': ['open_and_process_covid_data'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
