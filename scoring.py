"""
Name: The negative consequences of COVID-19 on NAICS categorized industries in Canada
Part: Scoring

Module Description
===============================
This module scores all industries in the gdp dataset.

Score1 represents how much they dropped down at the beginning of the covid. The more they dropped
down, the higher would their score1s be. For those industries who did not have any drop-down at the
beginning of the covid, they would be marked as special_industry and will be analyzed individually.

Score2 represents how many days it takes for each industry to recover back the gdp value before the
drop down if it is not been marked as special industry before. The longer time it needs, the higher
score it will get. By analysing the graphs for all industries, we notice that most industries' gdp
will continue its growth after the recovery date. So industries whose gdp get lower than the
beginning gdp after the recovery date will be considered as special_industry and will be analysed
individually.

Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for this project,
please email Paul.He@mail.utoronto.ca.

This file is Copyright (c) 2021 Paul He, Jiawei Yu and Xiling Zhao.
"""
import datetime
import math
from typing import Optional
import statistics
from open_up_the_file_for_industry import open_up_and_process_gdp_data, Industry


def output_score(filename: str) -> tuple[list, list, list]:
    """Output the score for every industry that is regular. The items in the first output list
    are the names of the industries; the items in the second output list are their score1s; the
    items in the third output list are their score2s."""
    global_industries = open_up_and_process_gdp_data(filename)
    # r means regular_industry, g means global_industries
    r, _, g = score_system(global_industries)
    recovery_industries(g)
    r, _ = score2(r)
    x, y1, y2 = [], [], []
    for industry in r:
        x.append(industry.name)
        y1.append(industry.score1)
        y2.append(industry.score2)
    return (x, y1, y2)


def score_system(industries: list[Industry]) -> \
        tuple[list[Industry], list[Industry], list[Industry]]:
    """The helper function of output_score
    Calculate score1 for every industry in the input list.
    return a tuple contains three lists:
        - first is the list contains all regular industries
        - second is the list contains all special industries
        - third is the original list industries instead the regular industries' score1 have been
          mutated.
    """
    regular_industry = []
    special_industry = []
    drop_down = []
    all_drop_down_percentage = drop_down_for_industries(industries, regular_industry,
                                                        special_industry)
    for industry in regular_industry:
        drop_down.append(all_drop_down_percentage[industry.name])
    average = statistics.mean(drop_down)
    for i in range(len(drop_down)):
        regular_industry[i].score1 = drop_down[i] / average * 10
    return regular_industry, special_industry, industries


def drop_down_for_industry(industry: Industry, regular_industry: list[Industry],
                           special_industry: list[Industry]) -> Optional[float]:
    """The helper function of score_system
    Calculate the percentage of the gdp first drop down based on the
    initial month if there is a drop down.
    """
    # set the gdp in the month before the covid as standard gdp
    standard = industry.gdp[datetime.date(2020, 3, 1)]
    minimum_gdp = math.inf
    # find the minimum gdp in the next three months after the covid happends.
    for i in range(4, 7):
        if industry.gdp[datetime.date(2020, i, 1)] < minimum_gdp:
            minimum_gdp = industry.gdp[datetime.date(2020, i, 1)]
    # if the industry's minimum gdp in next three months is even higher than the standard gdp,
    # it is not count as drop down and the special_industry append this industry.
    if minimum_gdp >= standard:
        special_industry.append(industry)
        return None
    # Otherwise, this industry would be added into the regular_industry. Return the percentage of
    # the drop down.
    else:
        regular_industry.append(industry)
        return minimum_gdp / standard - 1


def drop_down_for_industries(industries: list[Industry], regular_industry: list[Industry],
                             special_industry: list[Industry]) -> dict[str, float]:
    """The helper function of score_system
    Return a dictionary whose key is the name of the industry and value is the percentage
    of that industry's drop down compared to its gdp at March 1st 2020.
    """
    final = {}
    for industry in industries:
        a = drop_down_for_industry(industry, regular_industry, special_industry)
        # if a is not None, that means this industry is not be considered as special industry and
        # has drop down.
        if a is not None:
            final[industry.name] = a
    return final


def score2(industries: list[Industry]) -> tuple[list, list]:
    """The helper function of output_score
    Calculate the score2 for industries in the input list.
    """

    days, regular_industry, special_industry = recovery_industries(industries)

    # calculate the mean of days it takes for industries to recover
    mean = statistics.mean(list(days.values()))
    target = {}
    temp_industry = 0
    for industry in days:
        for x in regular_industry:
            # look for x in regular industry
            if x.name == industry:
                temp_industry = x
                break

        # give this industry a score2
        target[temp_industry.name] = days[temp_industry.name] / mean
        temp_industry.score2 = target[temp_industry.name] * 10
    return regular_industry, special_industry


def recovery_industries(industries=None) -> tuple[dict, list, list]:
    """The helper function of score2
    Output a dictionary that maps each industry's name to the number of days it takes to recover.
    The other two lists are output to keep track of which the regular/special industries are. """
    final = {}
    # assign industries needed to do the calculation.
    regular_industry, special_industry, industries = score_system(industries)
    for industry in industries:
        # calculate the number of days it takes for this industry to recover
        a = recovery_time(industry, regular_industry, special_industry)
        if industry in regular_industry:
            # assign the days to the industry's name in the output dictionary
            final[industry.name] = a
    return final, regular_industry, special_industry


def recovery_time(industry: Industry, regular_industry: list[Industry],
                  special_industry: list[Industry]) -> int:
    """The helper function of recovery_industries
    Return the number of days that the industry takes to get its gdp back to the initial gdp"""
    minimum_gdp = math.inf
    minimum_month = 0
    recovery_date = 0
    day_takes = 0

    # find the minimum of this industry's gdp
    for i in range(4, 7):
        if industry.gdp[datetime.date(2020, i, 1)] < minimum_gdp:
            minimum_gdp = industry.gdp[datetime.date(2020, i, 1)]
            minimum_month = i

    # initialize the timestamps that we need to do the gdp comparison
    timestamp = [datetime.date(2020, j, 1) for j in range(minimum_month, 13)]
    timestamp.extend([datetime.date(2021, k, 1) for k in range(1, 10)])
    index = 0

    for date in timestamp:
        # perform the gdp comparison needed to determine the number of days for the given industry
        # to recover
        if industry.gdp[date] >= industry.gdp[datetime.date(2020, 3, 1)]:
            day_takes = (date - datetime.date(2020, 3, 1)).days
            recovery_date = date
            index = timestamp.index(date)
            break

    if day_takes == 0:
        # if an industry had not recovered on Sep 1st, 2021, we assume its recovery date is
        # Sep 1st, 2021.
        recovery_date = datetime.date(2021, 9, 1)
        day_takes = (datetime.date(2021, 9, 1) - datetime.date(2020, 3, 1)).days

    if recovery_date != 0 and recovery_date != datetime.date(2021, 9, 1):
        # we determine whether this industry is special or regular
        for date in range(index + 1, len(timestamp)):
            if industry.gdp[timestamp[date]] < industry.gdp[datetime.date(2020, 3, 1)]:
                # if the industry is special, we then remove it from the regular industry list
                # and append it to the special industry list
                special_industry.append(industry)
                regular_industry.remove(industry)
                break
    return day_takes


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['csv', 'datetime', 'math', 'statistics',
                          'open_up_the_file_for_industry'],
        'allowed-io': ['open_up_and_process_gdp_data'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
