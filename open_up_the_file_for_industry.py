"""
Name: The negative consequences of COVID-19 on NAICS categorized industries in Canada
Part: open_up_the_file_for_industry

Module Description
==================
This module contains open up and store the data from the gdp datasets and make the right
output for the rest of the project program.

Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2021 Paul He, Jiawei Yu and Xiling Zhao."""

import datetime
import csv
from dataclasses import dataclass


@dataclass
class Industry:
    """A representation of a single industry.
    Instance Attribute:
        - name: a string representing the name of the industry
        - gdp: a dictionary mapping a date to an int, which is the gdp of that industry
               in the month of the date
        - score1: the score this industry obtains from our first scoring system
        - score2: the score this industry obtains from our second scoring system
    """
    name: str
    gdp: dict[datetime.date, int]
    score1: float
    score2: float


def open_up_and_process_gdp_data(file_name: str) -> list[Industry]:
    """
    The `main' function of the file, return data stored in a csv file with the given filename.

    The function could get all the industry data stored in the given file. This would:
    - get industry's name
    - get all months in the file as the key for dictionary and stored that month's gdp as the
    value of the dictionary
    - initialize all industry's score1 and score2 as 0.

    Preconditions:
      - filename refers to a valid csv file with headers
      - file represent the specific file be download by the given URL in the requirement
      - the month in the twelfth line must be in the format: 'mmmm yyyy' the first character
        in the month has to be capitalize
        for example: 'March 2020'
    """
    with open(file_name) as file:
        reader = list(csv.reader(file))
        list_of_industry = []
        industry = 0
        # only between line 14 and line 49 in the file are valuable and give us the data we need
        for i in range(13, 49):
            name = reader[i][0]
            # get gdp data for the industry, the key is the datetime.date, the value is the gdp
            # value in that month
            all_month_data_so_far = {}
            for j in range(1, len(reader[i])):
                date = convert_month_to_datetime(reader[11][j])
                # clean the file's data into the format which can be used int build-in method
                all_month_data_so_far[date] = int(reader[i][j].replace(',', ''))
                industry = Industry(name, all_month_data_so_far, 0, 0)
            list_of_industry.append(industry)
    return list_of_industry


def convert_month_to_datetime(name: str) -> datetime.date:
    """The helper funtion of open_up_and_process_gdp_data.
   Convert a string in 'mmmm yyyy' format to a datetime.time.

    Percondition:
        - name must to be the format: 'mmmm yyyy' the first character in the month has to be
        capitalize for example: 'March 2020'


    >>> convert_month_to_datetime('March 2020')
    datetime.date(2020, 3, 1)
    """
    date = str.split(name, ' ')
    month_english = date[0]
    month = 0
    if month_english == 'January':
        month = 1
    if month_english == 'February':
        month = 2
    if month_english == 'March':
        month = 3
    if month_english == 'April':
        month = 4
    if month_english == 'May':
        month = 5
    if month_english == 'June':
        month = 6
    if month_english == 'July':
        month = 7
    if month_english == 'August':
        month = 8
    if month_english == 'September':
        month = 9
    if month_english == 'October':
        month = 10
    if month_english == 'November':
        month = 11
    if month_english == 'December':
        month = 12
    year = int(date[1])
    return datetime.date(year, month, 1)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['csv', 'datetime'],
        'allowed-io': ['open_up_and_process_gdp_data'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
