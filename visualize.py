"""
Name: The negative consequences of COVID-19 on NAICS categorized industries in Canada
Part: visualize

Module Description
===============================
The module of producing covid line graph over time

Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for this project,
please email Paul.He@mail.utoronto.ca.

This file is Copyright (c) 2021 Paul He, Jiawei Yu and Xiling Zhao

"""

import datetime
from dataclasses import dataclass

import plotly.express as px
import pandas as pd


@dataclass
class Industry:
    """Dataclass Industry with attributes name and gdp"""
    name: str
    gdp: dict[datetime.date, int]


def sort_month(data: dict[datetime, int]) -> list[datetime]:
    """sorts datetime from past to present in order
    >>> data = {datetime.datetime(2230, 12, 1): 12121, datetime.datetime(2003, 1, 7): 9999}
    >>> sort_month(data)
    [datetime.datetime(2003, 1, 7, 0, 0), datetime.datetime(2230, 12, 1, 0, 0)]
    """
    return sorted(list(dict.keys(data)))


def sort_cases(sorted_month: list[datetime], data: dict[datetime, int]) -> list[int]:
    """match covid cases to its month
    >>> data = {datetime.datetime(2230, 12, 1): 9999, datetime.datetime(2003, 1, 1): 0}
    >>> x = sort_month(data)
    >>> sort_cases(x, data)
    [0, 9999]
    """
    sorted_so_far = []
    for month in sorted_month:
        sorted_so_far.append(data[month])
    return sorted_so_far


def plot_covid_month(data: dict[datetime, int]) -> None:
    """
     dataframe = pd.DataFrame(dict(
        month=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        covid_cases=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
    ))

    """
    # calls helper functions and sorts in order from oldest to most recent months in order
    sorted_month = sort_month(data)
    sorted_cases = sort_cases(sorted_month, data)

    # create a new dataframe with x axis month sorted and y axis sorted cases
    dataframe = pd.DataFrame(dict(
        month=sorted_month,
        covid_cases=sorted_cases
    ))
    # create and plot data
    figure = px.line(dataframe, x='month', y='covid_cases', title='Covid Cases per Month')
    figure.show()


####################################################################################################
# Graph 2
####################################################################################################

def industry_name(data: list[Industry]) -> list[str]:
    """Given a list of dataclass industry, return a list of industry names
    >>> airline = Industry('airline', {datetime.date(2020, 1, 1): 1, \
    datetime.date(2020, 2, 1): 20, datetime.date(2020, 3, 1): 30})
    >>> food = Industry('food', {datetime.date(2020, 1, 1): 1, \
    datetime.date(2020, 2, 1): 2, datetime.date(2020, 3, 1): 4})
    >>> industries = [airline, food]
    >>> industry_name(industries)
    ['airline', 'food']
    """
    return [industry.name for industry in data]


def industry_gdp(data: list[Industry]) -> list[dict[datetime.date, int]]:
    """Given a list of dataclass industry, return a list Industry's corresponding GDP
    >>> airline = Industry('airline', {datetime.date(2020, 1, 1): 1, \
    datetime.date(2020, 2, 1): 20, datetime.date(2020, 3, 1): 30})
    >>> food = Industry('food', {datetime.date(2020, 1, 1): 1, \
    datetime.date(2020, 2, 1): 2, datetime.date(2020, 3, 1): 4})
    >>> industries = [airline, food]
    >>> industry_gdp(industries)
    [{datetime.date(2020, 1, 1): 1, datetime.date(2020, 2, 1): 20, datetime.date(2020, 3, 1): 30}\
, {datetime.date(2020, 1, 1): 1, datetime.date(2020, 2, 1): 2, datetime.date(2020, 3, 1): 4}]
    """
    return [industry.gdp for industry in data]


def create_dataset(data: list[Industry]) -> dict[str, list]:
    """
    >>> airline = Industry('airline', {datetime.date(2020, 1, 1): 1000000, \
    datetime.date(2020, 2, 1): 20000,datetime.date(2020, 3, 1): 3000000})
    >>> food = Industry('food', {datetime.date(2020, 1, 1): 1000000,\
     datetime.date(2020, 2, 1): 20000,datetime.date(2020, 3, 1): 3000000})
    >>> industries = [airline, food]
    >>> create_dataset(industries)
    {'Industry': ['airline', 'airline', 'airline', 'food', 'food', 'food'], \
'Date': [datetime.date(2020, 1, 1), datetime.date(2020, 2, 1), datetime.date(2020, 3, 1), \
datetime.date(2020, 1, 1), datetime.date(2020, 2, 1), datetime.date(2020, 3, 1)], 'GDP': \
[1000000, 20000, 3000000, 1000000, 20000, 3000000]}
    """
    # retrieve industry name and gdp
    name = industry_name(data)
    gdp = industry_gdp(data)
    length = [len(x) for x in gdp]

    # append name, gdp into a dataset
    data = {'Industry': [], 'Date': [], 'GDP': []}
    for i in range(len(name)):
        count = 0
        while count < length[i]:
            data['Industry'].append(name[i])
            count += 1
    for d in gdp:
        dates = list(d.keys())
        gdp = [d[day] for day in dates]
        for date in dates:
            data['Date'].append(date)
        for g in gdp:
            data['GDP'].append(g)
    return data


if __name__ == '__main__':
    import doctest
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['dash', 'pandas', 'numpy', 'datetime', 'dash.dependencies',
                          'plotly.express',
                          'dataclasses',
                          'open_up_the_file_for_industry', 'visualize', 'scoring'],
        'allowed-io': ['open_up_and_process_data_for_gdp_v1', 'scoring'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })

    doctest.testmod()
